import pandas as pd
import json
import os
import csv
import sys
import pickle
import zipfile
import requests
import shutil
import base64

from pathlib import Path
sys.path.append(os.path.abspath('../'))
import util, read_datasets, main_fairER, main_unfair, statistics


def runFairER(dataset, explanation):
    """
        Runs main_fairER.py pipeline and produces the evaluation results, predictions and clusters 

        Produced data:  (web/data/json_data/evaluation_data.json), 
                        (web/data/json_data/preds_data.json),
                        (web/data/json_data/clusters_data.json)

        Parameter dataset: the dataset.
        Precondition: dataset is String.

        Parameter explanation: The need for explanation.
        Precondition: explanation is Integer, with two possible values: "0", "1".
    """
    cur_dir = os.path.abspath(".")
    if int(explanation) == 0:
        main_fairER.main(os.path.join(cur_dir, '..', 'resources','Datasets',dataset), 'joined_train.csv', 'joined_valid.csv', 'joined_test.csv', explanation)
    else:
        main_fairER.main(os.path.join(cur_dir, '..', 'resources','Datasets',dataset), 'merged_train.csv', 'merged_valid.csv', 'merged_test.csv', explanation)


def runUnfair(dataset):
    """
        Runs main_unfair.py pipeline and produces the evaluation results, predictions and clusters 

        Produced data:  (web/data/json_data/evaluation_data.json), 
                        (web/data/json_data/preds_data.json),
                        (web/data/json_data/clusters_data.json)

        Parameter dataset: the dataset.
        Precondition: dataset is String.
    """
    cur_dir = os.path.abspath(".")
    main_unfair.main(os.path.join(cur_dir, '..', 'resources','Datasets',dataset), 'joined_train.csv', 'joined_valid.csv', 'joined_test.csv', 20) # k==20




def runStatistics(dataset):
    """
        Produces the statistics for a specific dataset 
        
        Produced data: (web/data/json_data/statistics_data.json)

        Parameter dataset: the dataset.
        Precondition: dataset is String.
    """
    statistics.main(dataset)





def getAccuracy(algo, dataset, explanation):
    """
        Returns the accuracy for a specific dataset
        
        Parameter algo: Which pipeline to run.
        Precondition: algo is String, with two possible values: "fairER", "unfair".

        Parameter dataset: the dataset.
        Precondition: dataset is String.

        Parameter explanation: The need for explanation.
        Precondition: explanation is Integer, with two possible values: "0", "1".
    """
    if algo == 'fairER':
        runFairER(dataset, explanation)
    else:
        runUnfair(dataset)
    with open('data/json_data/evaluation_data.json') as json_file:
        data = json.load(json_file)
    return str(data['accuracy'])




def getEOD(algo, dataset, explanation):
    """
        Returns the EOD for a specific dataset
        
        Parameter algo: Which pipeline to run.
        Precondition: algo is String, with two possible values: "fairER", "unfair".

        Parameter dataset: the dataset.
        Precondition: dataset is String.

        Parameter explanation: The need for explanation.
        Precondition: explanation is Integer, with two possible values: "0", "1".
    """
    if algo == 'fairER':
        runFairER(dataset, explanation)
    else:
        runUnfair(dataset)
    with open('data/json_data/evaluation_data.json') as json_file:
        data = json.load(json_file)
    return str(data['EOD'])




def getSPD(algo, dataset, explanation):
    """
        Returns the SPD for a specific dataset
        
        Parameter algo: Which pipeline to run.
        Precondition: algo is String, with two possible values: "fairER", "unfair".

        Parameter dataset: the dataset.
        Precondition: dataset is String.

        Parameter explanation: The need for explanation.
        Precondition: explanation is Integer, with two possible values: "0", "1".
    """
    if algo == 'fairER':
        runFairER(dataset, explanation)
    else:
        runUnfair(dataset)
    with open('data/json_data/evaluation_data.json') as json_file:
        data = json.load(json_file)
    return str(data['SPD'])





def protectedCond(dataset, explanation):
    data = {}
    if explanation == 0:
        pickle_path = os.path.join('data', 'pickle_data', 'protected_conditions.pkl')
    else:
        pickle_path = os.path.join('data', 'pickle_data', 'protected_conditions_w_exp.pkl')
    curr_dir = os.path.split(os.getcwd())[1]
    if curr_dir == 'fairER':
        pickle_path = 'web/' + pickle_path
    if os.path.exists(pickle_path) and os.path.getsize(pickle_path) > 0:
        with open(pickle_path, 'rb') as pkl_file:
            data = pickle.load(pkl_file)

    condition = data.get(dataset)
    return condition


def hasCustomCond(dataset):
    data = {}
    pickle_path = 'data/pickle_data/protected_conditions.pkl'
    if os.path.exists(pickle_path) and os.path.getsize(pickle_path) > 0:
        with open(pickle_path, 'rb') as pkl_file:
            data = pickle.load(pkl_file)

    condition = data.get(dataset)
    if condition == None:
        return False
    else:
        return True




def csv_to_json(csvFilePath, jsonFilePath):
    """
        Converts a csv file to json
        
        Parameter csvFilePath: CSV file path (input).

        Parameter jsonFilePath: JSON file path (output).
    """
    jsonArray = []
    # read csv file
    with open(csvFilePath, encoding='utf-8') as csvFile:
        # load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvFile)

        # convert each csv row into python dict
        for row in csvReader:
            # add this python dict to json array
            jsonArray.append(row)

    # convert python jsonArray to JSON String and write to file
    with open(jsonFilePath, 'w+', encoding='utf-8') as jsonFile:
        jsonString = json.dumps(jsonArray, indent=4)
        jsonFile.write(jsonString)




def checkTupleProtected(dataset, arg, json_obj):
    """
        Returns whether the tuple is protected.
        
        Parameter dataset: the dataset.

        Parameter arg: "left" or "right" tuple

        Parameter json_obj: contains the values for every attribute of this tuple
    """
    key = []
    value = []
    if arg == 'right':
        otherSide = 'left'
    else:
        otherSide = 'right'

    for data in json_obj:
        key.append(arg + "_" + list(data.keys())[0])
        value.append(data.get(list(data.keys())[0]))
        key.append(otherSide + "_" + list(data.keys())[0])
        value.append('')

    df = pd.DataFrame(columns=key)
    for i in range(len(json_obj)*2):
        this_column = df.columns[i]
        df[this_column] = [value[i]]

    return util.pair_is_protected(df, dataset, False)


def getAttributes(table, dataset):
    """
        Returns the attributes of the header of a specific table (right or left) of a dataset.

        Parameter table: "left" or "right" tuple
        
        Parameter dataset: the dataset.
    """
    
    if table == 'right':
        file = 'tableA.csv'
    else:
        file = 'tableB.csv'
    with open('../resources/Datasets/'+dataset+'/'+file, errors='ignore') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        list_of_column_names = []

        # iterate through the rows of csv
        for row in csv_reader:
            list_of_column_names.append(row)
            break  # break the loop after the first iteration

        list_of_column_names[0].pop(0)  # we dont want 'id' attribute

        jsonString = json.dumps(list_of_column_names[0])
    return jsonString


def check_tuple_attributes(dataset, table, tuple):
    dataset_attributes = getAttributes(table, dataset)
    tuple_attributes = []
    for data in tuple:
        tuple_attributes.append(list(data.keys())[0])

    for data in tuple_attributes:
        if data not in dataset_attributes:
            return False
    return True




def saveNewCond(dataset, condition, condition_w_exp):
    data = {}
    data_w_exp = {}
    pickle_path = os.path.join('data', 'pickle_data', 'protected_conditions.pkl')
    pickle_w_exp_path = os.path.join('data', 'pickle_data', 'protected_conditions_w_exp.pkl')
    curr_dir = os.path.split(os.getcwd())[1]
    if curr_dir == 'fairER':
        pickle_path = 'web/' + pickle_path

    if os.path.exists(pickle_path) and os.path.getsize(pickle_path) > 0:
        with open(pickle_path, 'rb') as pkl_file:
            data = pickle.load(pkl_file)
        with open(pickle_w_exp_path, 'rb') as pkl_file_w_exp:
            data_w_exp = pickle.load(pkl_file_w_exp)

    data[dataset] = condition
    data_w_exp[dataset] = condition_w_exp
    with open(pickle_path, 'wb') as pkl_file:
        pickle.dump(data, pkl_file, protocol=pickle.HIGHEST_PROTOCOL)
    with open(pickle_w_exp_path, 'wb') as pkl_file_w_exp:
        pickle.dump(data_w_exp, pkl_file_w_exp, protocol=pickle.HIGHEST_PROTOCOL)


def condInFile(dataset):
    data = {}
    pickle_path = os.path.join('data', 'pickle_data', 'protected_conditions.pkl')

    curr_dir = os.path.split(os.getcwd())[1]
    if curr_dir == 'fairER':
        pickle_path = 'web/' + pickle_path

    if os.path.exists(pickle_path) and os.path.getsize(pickle_path) > 0:
        with open(pickle_path, 'rb') as pkl_file:
            data = pickle.load(pkl_file)
            if dataset not in data:
                return False
            else:
                return True
    else:
        return False


def deleteCachedData(dataset):
    """
        Deletes every cached file of a given dataset.
    """
    cur_dir = os.path.abspath(".")
        
    best_model_w_explainer_path = Path(os.path.join(cur_dir, '..', 'resources', 'Datasets', dataset, 'best_model_w_explainer.pth'))
    best_model_path = Path(os.path.join(cur_dir, '..', 'resources', 'Datasets', dataset, 'best_model.pth'))
    cached_data_path = Path(os.path.join(cur_dir, '..', 'resources', 'Datasets', dataset, 'cacheddata.pth'))
    dm_results_path = Path(os.path.join(cur_dir, '..', 'resources', 'Datasets', dataset, 'dm_results.csv'))
    figure_1_path = Path(os.path.join(cur_dir, '..', 'resources', 'Datasets', dataset, 'figures', 'Figure_1.png'))
    figure_2_path = Path(os.path.join(cur_dir, '..', 'resources', 'Datasets', dataset, 'figures', 'Figure_2.png'))

    if os.path.exists(best_model_w_explainer_path):
        os.remove(best_model_w_explainer_path)
    if os.path.exists(best_model_path):
        os.remove(best_model_path)
    if os.path.exists(cached_data_path):
        os.remove(cached_data_path)
    if os.path.exists(dm_results_path):
        os.remove(dm_results_path)
    if os.path.exists(figure_1_path):
        os.remove(figure_1_path)
    if os.path.exists(figure_2_path):
        os.remove(figure_2_path)






def eval_to_json(accuracy, spd, eod):
    """
        Writes the evaluation results  to a json file.
    """
    data = {'accuracy': accuracy, 'SPD': spd, 'EOD': eod}
    json_string = json.dumps(data)
    with open('data/json_data/evaluation_data.json', 'w+') as outfile:
        outfile.write(json_string)





def clusters_to_json(clusters):
    """
        Writes the clusters to a json file.
    """
    json_string = '['
    for i in clusters:
        json_string = json_string + '{"Table A":"'+str(i[0])+'" , "Table B":"'+str(i[1])+'"},'
    
    json_string = json_string + ']'

    data = {"clusters": json_string}

    json_string = json.dumps(data)
    with open('data/json_data/clusters_data.json', 'w+') as outfile:
        outfile.write(json_string)


def preds_to_json(data_path):
    """
        Writes the predictions to a json file.
    """
    csv_to_json(data_path + '/dm_results.csv',
                'data/json_data/preds_data.json') 





def extract_dataset(filename):
    """
        Creates a new directory named as the dataset's zip name, 
        and extracts the zip file to this new dir.
    """
    dataset_path = os.path.join('data', 'datasets')

    # new directory name 
    directory = os.path.splitext(filename)[0]

    cur_dir = os.path.abspath(".")
    path = os.path.join(cur_dir, '..',  'resources', 'Datasets', directory)
    os.mkdir(path)
    figures_path = os.path.join(path, 'figures')
    os.mkdir(figures_path)
    
    with zipfile.ZipFile(os.path.join(dataset_path, filename), 'r') as zip_ref:
        zip_ref.extractall(path)




def check_for_duplicates(filename):
    filename = os.path.splitext(filename)[0]
    cur_dir = os.path.abspath(".")
    parent_dir = Path(os.getcwd()).parent.absolute()
    os.chdir(parent_dir)
    exists = os.path.exists(os.path.join('resources', 'Datasets', filename))
    if not exists:
        os.chdir(cur_dir)
        return True 
    else:
        os.chdir(cur_dir)
        return False


def delete_dataset_zip(filename):
    """
        Deletes the downloaded zip file
    """
    path = os.path.join('data', 'datasets', filename)
    if os.path.exists(path):
        os.remove(path)



def datasets_names_to_json():
    """
        Returns a list with the names of all the available datasets
    """
    datasets_list = [] 
    cur_dir = os.path.abspath(".")
    rootdir = os.path.join(cur_dir, '..', 'resources', 'Datasets')

    for path in Path(rootdir).iterdir():
        if path.is_dir():
            datasets_list.append(os.path.basename(path))

    return datasets_list




def datasets_without_condition():
    non_deepmatcher_datasets = []
    datasets_without_condition = []
    deepmatcher_datasets = ["DBLP-ACM", "Amazon-Google", "iTunes-Amazon", "Beer", "Fodors-Zagats", "Walmart-Amazon", "DBLP-GoogleScholar"]
    datasets_list = datasets_names_to_json()
    for item in datasets_list:
        if item not in deepmatcher_datasets:
            non_deepmatcher_datasets.append(item)

    

    pickle_path = os.path.join('data', 'pickle_data', 'protected_conditions.pkl')

    if os.path.exists(pickle_path) and os.path.getsize(pickle_path) > 0:
        with open(pickle_path, 'rb') as pkl_file:
            data = pickle.load(pkl_file)
            for item in non_deepmatcher_datasets:
                if item not in data:
                    datasets_without_condition.append(item)
                    
    else: 
        return non_deepmatcher_datasets

    return datasets_without_condition


    

def non_cached_datasets():
    non_cached_datasets = []

    parent_dir = Path(os.getcwd()).parent.absolute()
    os.chdir(parent_dir)
    datasets_dir = os.path.join('resources', 'Datasets')
    for path in Path(datasets_dir).iterdir():
        if path.is_dir():
            dm_results = os.path.join(path, 'dm_results.csv')
            if not os.path.isfile(dm_results):
                non_cached_datasets.append(os.path.basename(path))
    
    os.chdir(os.path.join(os.getcwd(),'web'))
    return non_cached_datasets




def download_dataset():
    """
        Downloads and sets up all the DM datasets from https://github.com/anhaidgroup/deepmatcher/blob/master/Datasets.md
    """
    Beer_url = 'http://pages.cs.wisc.edu/~anhai/data1/deepmatcher_data/Structured/Beer/beer_exp_data.zip'
    downloaded_obj = requests.get(Beer_url)
    with open(os.path.join('data', 'datasets', 'Beer.zip'), "wb") as file:
        file.write(downloaded_obj.content)
    extract_dataset('Beer.zip')
    delete_dataset_zip('Beer.zip')
    export_exp_data('Beer')

    iTunes_Amazon_url = 'http://pages.cs.wisc.edu/~anhai/data1/deepmatcher_data/Structured/iTunes-Amazon/itunes_amazon_exp_data.zip'
    downloaded_obj = requests.get(iTunes_Amazon_url)
    with open(os.path.join('data', 'datasets', 'iTunes-Amazon.zip'), "wb") as file:
        file.write(downloaded_obj.content)
    extract_dataset('iTunes-Amazon.zip')
    delete_dataset_zip('iTunes-Amazon.zip')
    export_exp_data('iTunes-Amazon')
    
    
    DBLP_ACM_url = 'http://pages.cs.wisc.edu/~anhai/data1/deepmatcher_data/Structured/DBLP-ACM/dblp_acm_exp_data.zip'
    downloaded_obj = requests.get(DBLP_ACM_url)
    with open(os.path.join('data', 'datasets', 'DBLP-ACM.zip'), "wb") as file:
        file.write(downloaded_obj.content)
    extract_dataset('DBLP-ACM.zip')
    delete_dataset_zip('DBLP-ACM.zip')
    export_exp_data('DBLP-ACM')
    
    DBLP_GoogleScholar_url = 'http://pages.cs.wisc.edu/~anhai/data1/deepmatcher_data/Structured/DBLP-GoogleScholar/dblp_scholar_exp_data.zip'
    downloaded_obj = requests.get(DBLP_GoogleScholar_url)
    with open(os.path.join('data', 'datasets', 'DBLP-GoogleScholar.zip'), "wb") as file:
        file.write(downloaded_obj.content)
    extract_dataset('DBLP-GoogleScholar.zip')
    delete_dataset_zip('DBLP-GoogleScholar.zip')
    export_exp_data('DBLP-GoogleScholar')

    Amazon_Google_url = 'http://pages.cs.wisc.edu/~anhai/data1/deepmatcher_data/Structured/Amazon-Google/amazon_google_exp_data.zip'
    downloaded_obj = requests.get(Amazon_Google_url)
    with open(os.path.join('data', 'datasets', 'Amazon-Google.zip'), "wb") as file:
        file.write(downloaded_obj.content)
    extract_dataset('Amazon-Google.zip')
    delete_dataset_zip('Amazon-Google.zip')
    
    Walmart_Amazon_url = 'http://pages.cs.wisc.edu/~anhai/data1/deepmatcher_data/Structured/Walmart-Amazon/walmart_amazon_exp_data.zip'
    downloaded_obj = requests.get(Walmart_Amazon_url)
    with open(os.path.join('data', 'datasets', 'Walmart-Amazon.zip'), "wb") as file:
        file.write(downloaded_obj.content)
    extract_dataset('Walmart-Amazon.zip')
    delete_dataset_zip('Walmart-Amazon.zip')
    export_exp_data('Walmart-Amazon')


    
def read_dm_datasets():
    """
        Reads all the DM datasets to produce the "joined_" files.
    """
    read_datasets.run('Beer')
    read_datasets.run('iTunes-Amazon')
    read_datasets.run('DBLP-ACM')
    read_datasets.run('DBLP-GoogleScholar')
    read_datasets.run('Amazon-Google')
    read_datasets.run('Walmart-Amazon')




def read_uploaded_dataset(dataset):
    read_datasets.run(dataset)



def export_exp_data(dataset):
    """
        Copies the files from "exp_data" to the dataset's directory.
    """
    cur_dir = os.path.abspath(".")
    file_source = os.path.join(cur_dir, '..', 'resources', 'Datasets', dataset, 'exp_data')
    file_destination = os.path.join(cur_dir, '..', 'resources', 'Datasets', dataset)
    
    shutil.copy(os.path.join(file_source,'tableA.csv'), file_destination)
    shutil.copy(os.path.join(file_source,'tableB.csv'), file_destination)
    shutil.copy(os.path.join(file_source,'valid.csv'), file_destination)
    shutil.copy(os.path.join(file_source,'test.csv'), file_destination)
    shutil.copy(os.path.join(file_source,'train.csv'), file_destination)
    shutil.rmtree(file_source) #delete forled 'exp_data'




def img_to_base64(dataset, figure):
    """
        Encodes (base64) and returns an image file.
        
        Parameter dataset: To check for the image to the specific folder

        Parameter figure: Which one of the figures ("Figure_1.png" or "Figure_2.png")
    """
    cur_dir = os.path.abspath(".")
    path_to_figure = os.path.join(cur_dir, '..', 'resources', 'Datasets', dataset, 'figures', figure)
    with open(path_to_figure, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    return encoded_string.decode('utf-8')





def explanation_exists(dataset):
    """
        Returns whether the explanation exists.
    """
    cur_dir = os.path.abspath(".")
    path_to_figure = os.path.join(cur_dir, '..', 'resources', 'Datasets', dataset, 'figures', 'Figure_1.png')
    exists = os.path.exists(path_to_figure)
    return exists




def construct_cond(left_attribute, left_func, left_value, logical_op, right_attribute, right_func, right_value, explanation):
    if explanation == 0:
        if left_func == 'startswith': 
            left_part = '(str(tuple.left_'+left_attribute+').startswith(\''+left_value+'\'))'
        else:
            left_part = '(\''+left_value+'\' '+left_func+' str(tuple.left_'+left_attribute+'))'

        if right_func == 'startswith': 
            right_part = '(str(tuple.right_'+right_attribute+').startswith(\''+right_value+'\'))'
        else:
            right_part = '(\''+right_value+'\' '+right_func+' str(tuple.right_'+right_attribute+'))'
    else:
        if left_func == 'startswith': 
            left_part = '(str(tuple.ltable_'+left_attribute+').startswith(\''+left_value+'\'))'
        else:
            left_part = '(\''+left_value+'\' '+left_func+' str(tuple.ltable_'+left_attribute+'))'

        if right_func == 'startswith': 
            right_part = '(str(tuple.rtable_'+right_attribute+').startswith(\''+right_value+'\'))'
        else:
            right_part = '(\''+right_value+'\' '+right_func+' str(tuple.rtable_'+right_attribute+'))'

    return left_part+' '+logical_op+' '+right_part 

def delete_dataset(dataset):
    cur_dir = os.path.abspath(".")
    parent_dir = Path(os.getcwd()).parent.absolute()
    os.chdir(parent_dir)
    


    path = os.path.join('resources', 'Datasets', dataset)
    if os.path.isdir(path):
        shutil.rmtree(path)
        os.chdir(cur_dir) 
        delete_condition_from_file(dataset)
        return True
    else:
        os.chdir(cur_dir) 
        return False
    
def delete_condition_from_file(dataset):
    data = {}
    data_w_exp = {}
    pickle_path = os.path.join('data', 'pickle_data', 'protected_conditions.pkl')
    pickle_w_exp_path = os.path.join('data', 'pickle_data', 'protected_conditions_w_exp.pkl')

    if os.path.exists(pickle_path) and os.path.getsize(pickle_path) > 0:
        with open(pickle_path, 'rb') as pkl_file:
            data = pickle.load(pkl_file)
        with open(pickle_w_exp_path, 'rb') as pkl_file_w_exp:
            data_w_exp = pickle.load(pkl_file_w_exp)

    if dataset in data:
        del data[dataset]
    if dataset in data_w_exp:
        del data_w_exp[dataset]

    with open(pickle_path, 'wb') as pkl_file:
        pickle.dump(data, pkl_file, protocol=pickle.HIGHEST_PROTOCOL)
    with open(pickle_w_exp_path, 'wb') as pkl_file_w_exp:
        pickle.dump(data_w_exp, pkl_file_w_exp, protocol=pickle.HIGHEST_PROTOCOL)
    