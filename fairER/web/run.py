from concurrent.futures import thread
import inspect
from pathlib import Path
from flask import Flask, render_template, request, json
from werkzeug.utils import secure_filename
import library.methods as methods
import sys, os
sys.path.append(os.path.abspath('../'))
import util

app = Flask(__name__)
UPLOAD_DATASET_FOLDER = 'web/data/datasets'
UPLOAD_JSON_FOLDER = 'web/data/datasets'
ALLOWED_EXTENSIONS = {'json', 'zip'}


# Navigate user to the services page
@app.route('/')
def services():
    return render_template('services.html')

# Navigate user to the services manual page
@app.route('/services-manual')
def manual():
    return render_template('manual.html')




@app.route("/requests/getAccuracy")
def getAccuracy():
    """
        Returns the accuracy.

        The response is in JSON format.

        Parameter dataset: the dataset.
        Precondition: dataset is String.

        Parameter alg: The algorithm to run.
        Precondition: alg is a String, with two possible values: "fairER", "unfair"
    """
    try:
        dataset = request.args.get('dataset')
        alg = request.args.get('alg')
        explanation = request.args.get('explanation')
        accuracy = methods.getAccuracy(alg, dataset, explanation)

        response = app.response_class(
            response=json.dumps(
                {'Algorithm': alg, 'Dataset': dataset, 'Accuracy': accuracy}, sort_keys=False),
            mimetype='application/json'
        )
        return response
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        func_name = inspect.stack()[0][3]
        response = app.response_class(
            response=json.dumps({'exception_type': str(exception_type), 'exception': str(e),
                                'func_name': str(func_name+'()'), 'filename': str(filename),
                                 'line_number': str(line_number)}),
            mimetype='application/json'
        )
        return response





@app.route("/requests/getSPD")
def getSPD():
    """
        Returns the SPD.

        The response is in JSON format.

        Parameter dataset: the dataset.
        Precondition: dataset is String.

        Parameter alg: The algorithm to run.
        Precondition: alg is a String, with two possible values: "fairER", "unfair"
    """
    try:
        dataset = request.args.get('dataset')
        alg = request.args.get('alg')
        explanation = request.args.get('explanation')
        spd = methods.getSPD(alg, dataset, explanation)
        
        response = app.response_class(
            response=json.dumps(
                {'Algorithm': alg, 'Dataset': dataset, 'SPD': spd}, sort_keys=False),
            mimetype='application/json'
        )
        return response
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        func_name = inspect.stack()[0][3] 
        response = app.response_class(
            response=json.dumps({'exception_type': str(exception_type), 'exception': str(e),
                                'func_name': str(func_name+'()'), 'filename': str(filename),    
                                'line_number': str(line_number)}),
            mimetype='application/json'
        )
        return response



@app.route("/requests/getEOD")
def getEOD():
    """
        Returns the EOD.

        The response is in JSON format.

        Parameter dataset: the dataset.
        Precondition: dataset is String.

        Parameter alg: The algorithm to run.
        Precondition: alg is a String, with two possible values: "fairER", "unfair"
    """
    try:
        dataset = request.args.get('dataset')
        alg = request.args.get('alg')
        explanation = request.args.get('explanation')
        eod = methods.getEOD(alg, dataset, explanation)
        
        response = app.response_class(
            response=json.dumps(
                {'Algorithm': alg, 'Dataset': dataset, 'EOD': eod}, sort_keys=False),
            mimetype='application/json'
        )
        return response
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        func_name = inspect.stack()[0][3] 
        response = app.response_class(
            response=json.dumps({'exception_type': str(exception_type), 'exception': str(e),
                                'func_name': str(func_name+'()'), 'filename': str(filename),    
                                'line_number': str(line_number)}),
            mimetype='application/json'
        )
        return response



@app.route("/requests/getEvaluationResults")
def getEvaluationResults():
    """
        Returns the Evaluation Results (accuracy, SPD, EOD).

        The response is in JSON format.

        Parameter dataset: the dataset.
        Precondition: dataset is String.

        Parameter alg: The algorithm to run.
        Precondition: alg is a String, with two possible values: "fairER", "unfair"
    """
    
    dataset = request.args.get('dataset')
    alg = request.args.get('alg')
    method = request.args.get('method')
    explanation = request.args.get('explanation')
    p = request.args.get('p')
    s = request.args.get('s')
    t = request.args.get('t')
    k = request.args.get('k')
    
    print(request.args)
    if p == None:
        conf = "original"
    else:
        conf = p + "_" + s + "_" + t

    if method == "deepmatcher":
        if alg == 'fairER':
                methods.runFairER(dataset, explanation, k)
        else:
                methods.runUnfair(dataset, k)
    elif method == "RREA" or method == "BERT_INT":
        if alg == 'fairER':
                methods.runFairER_RREA(dataset, explanation, conf, k, method=method)
        else:
                methods.runUnfair_RREA(dataset, explanation, conf, k, method=method)
    elif method == "RDGCN" or method == "MultiKE" or method == "PARIS":
            if alg == 'fairER':
                    methods.runFairER_OpenEA(dataset, explanation, conf, method, k)
            else:
                    methods.runUnfair_OpenEA(dataset, explanation, conf, method, k)
    # open the file that was created
    with open(os.path.join(os.getcwd(), 'web', 'data', 'json_data', 'evaluation_data.json')) as json_file:
            data = json.load(json_file)  # get the data from this file

    accuracy = str(data['accuracy'])
    spd = str(data['SPD'])
    eod = str(data['EOD'])

    response = app.response_class(
            response=json.dumps({'Algorithm': alg, 'Dataset': dataset,
                                'Accuracy@' + k: accuracy, 'SPD@' + k: spd, 'EOD@' + k: eod}, sort_keys=False),
            mimetype='application/json'
        )
    return response
     
     
    
    


@app.route('/requests/getPreds', methods=['GET'])
def getPreds():
    """
        Returns the Predictions.

        The response is in JSON format.

        Parameter dataset: the dataset.
        Precondition: dataset is String.

        Parameter alg: The algorithm to run.
        Precondition: alg is a String, with two possible values: "fairER", "unfair"
    """
    try:
        dataset = request.args.get('dataset')
        alg = request.args.get('alg')
        method = request.args.get('method')
        explanation = request.args.get('explanation')
        # p = request.args.get('p')
        # s = request.args.get('s')
        # t = request.args.get('t')
        # print(request.args)
        # if p == None:
        #     conf = "original"
        # else:
        #     conf = p + "_" + s + "_" + t
        conf = "original"
        if method == "deepmatcher":
            if alg == 'fairER':
                methods.runFairER(dataset, explanation)  
            else:
                methods.runUnfair(dataset) 
        # elif method == "RREA":
        #     if alg == 'fairER':
        #             methods.runFairER_RREA(dataset, explanation, conf)
        #     else:
        #             methods.runUnfair_RREA(dataset, explanation, conf)
        # elif method == "RDGCN" or method == "MultiKE":
        #     if alg == 'fairER':
        #             methods.runFairER_OpenEA(dataset, explanation, conf, method)
        #     else:
        #             methods.runUnfair_OpenEA(dataset, explanation, conf, method)


        # open the file that was created
        with open(os.path.join(os.getcwd() + '/web/' + 'data', 'json_data', 'preds_data.json')) as json_file:
            data = json.load(json_file)  # get the data from this file

        response = app.response_class(
            response=json.dumps({'preds': str(data)}),
            mimetype='application/json'
        )
        return response
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        func_name = inspect.stack()[0][3] 
        response = app.response_class(
            response=json.dumps({'exception_type': str(exception_type), 'exception': str(e),
                                'func_name': str(func_name+'()'), 'filename': str(filename),    
                                'line_number': str(line_number)}),
            mimetype='application/json'
        )
        return response



@app.route('/requests/getClusters', methods=['GET'])
def getClust():
    """
        Returns the Clusters.

        The response is in JSON format.

        Parameter dataset: the dataset.
        Precondition: dataset is String.

        Parameter alg: The algorithm to run.
        Precondition: alg is a String, with two possible values: "fairER", "unfair"
    """
    try:

        dataset = request.args.get('dataset')
        alg = request.args.get('alg')
        method = request.args.get('method')
        explanation = request.args.get('explanation')
        p = request.args.get('p')
        s = request.args.get('s')
        t = request.args.get('t')
        print(request.args)
        if p == None:
            conf = "original"
        else:
            conf = p + "_" + s + "_" + t

        if method == "deepmatcher":
            if alg == 'fairER':
                methods.runFairER(dataset, explanation)  
            else:
                methods.runUnfair(dataset) 
        elif method == "RREA" or method == "BERT_INT":
            if alg == 'fairER':
                    methods.runFairER_RREA(dataset, explanation, conf, method=method)
            else:
                    methods.runUnfair_RREA(dataset, explanation, conf, method=method)
        elif method == "RDGCN" or method == "MultiKE" or method == "PARIS":
            if alg == 'fairER':
                    methods.runFairER_OpenEA(dataset, explanation, conf, method)
            else:
                    methods.runUnfair_OpenEA(dataset, explanation, conf, method)

        with open(os.path.join(os.getcwd() + '/web/' + 'data', 'json_data', 'clusters_data.json')) as json_file:
            data = json.load(json_file)

        response = app.response_class(
            response=json.dumps({'clusters': str(data["clusters"])}),
            mimetype='application/json'
        )
        return response
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        func_name = inspect.stack()[0][3]
        response = app.response_class(
            response=json.dumps({'exception_type': str(exception_type), 'exception': str(e),
                                'func_name': str(func_name+'()'), 'filename': str(filename),
                                 'line_number': str(line_number)}),
            mimetype='application/json'
        )
        return response



@app.route('/requests/getStatistics', methods=['GET'])
def getStats():
    """
        Returns the Statistics for a dataset.

        The response is in JSON format.

        Parameter dataset: the dataset.
        Precondition: dataset is String.
    """
    try:
        dataset = request.args.get('dataset')
        dataset_type = request.args.get('type')
        explanation = request.args.get('explanation')

        if dataset_type == "tab":

            cur_dir = os.path.abspath(".")

            dm_results = os.path.join(
                cur_dir, 'resources', 'Datasets', dataset, 'dm_results.csv')

            if not os.path.isfile(dm_results):
                methods.runFairER(dataset, explanation)

            methods.runStatistics(dataset, dataset_type)
            with open(os.path.join('web', 'data', 'json_data', 'statistics_data.json')) as json_file:
                data = json.load(json_file)

            response = app.response_class(
                response=json.dumps({'Number of Protected Matches': data['num_protected_matches'],
                                    'Number of non-Protected Matches':  data['num_nonprotected_matches'],
                                    'Avg Score Protected': data['avg_score_protected'],
                                    'Avg Score non-Protected': data['avg_score_nonprotected'],
                                    'Avg Score Protected Matches': data['avg_score_protected_matches'],
                                    'Avg Score non-Protected Matches': data['avg_score_nonprotected_matches']}, sort_keys=False),
                mimetype='application/json'
            )

        elif dataset_type == "kg":

            p = request.args.get('p')
            if p == None:
                conf = "original"
            else:
                s = request.args.get('s')
                t = request.args.get('t')
                conf = p + "_" + s + "_" + t

            methods.runStatistics(dataset, dataset_type, conf)
            with open(os.path.join('web', 'data', 'json_data', 'statistics_data.json')) as json_file:
                data = json.load(json_file)

            response = app.response_class(
                response=json.dumps({'#Ents': data['#Nodes KG1'] + " / " + data['#Nodes KG2'],
                                    '#Rels':  data['#Relations KG1'] + " / " + data['#Relations KG2'],
                                    '#Triples':  data['#Triples KG1'] + " / " + data['#Triples KG2'],
                                    'wccR':  data['wccR KG1'] + " / " + data['wccR KG2'],
                                    'maxCS':  data['maxCS KG1'] + " / " + data['maxCS KG2'],
                                    'deg':  data['deg KG1'] + " / " + data['deg KG2']}, sort_keys=False),
                mimetype='application/json')
            
        return response
        
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        func_name = inspect.stack()[0][3] 
        response = app.response_class(
            response=json.dumps({'exception_type': str(exception_type), 'exception': str(e),
                                'func_name': str(func_name+'()'), 'filename': str(filename),    
                                'line_number': str(line_number)}),
            mimetype='application/json'
        )
    return response





@app.route("/requests/getProtectedCondition")
def getProtectedCondition():
    """
        Returns the Protected Condition for a dataset.

        The response is in JSON format.

        Parameter dataset: the dataset.
        Precondition: dataset is String.
    """
    try:
        dataset = request.args.get('dataset')
        result = util.pair_is_protected(
            tuple=None, dataset=dataset, return_condition=True)
        response = app.response_class(
            response=json.dumps({'condition': str(result)}),
            mimetype='application/json'
        )
        return response
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        func_name = inspect.stack()[0][3] 
        response = app.response_class(
            response=json.dumps({'exception_type': str(exception_type), 'exception': str(e),
                                'func_name': str(func_name+'()'), 'filename': str(filename),    
                                'line_number': str(line_number)}),
            mimetype='application/json'
        )
        return response





@app.route("/requests/getTableAttributes")
def getTablesAttributes():
    """
        Returns the attributes of the header of a specific table.

        The response is in JSON format.

        Parameter dataset: the dataset.
        Precondition: dataset is String.

        Parameter table: The table.
        Precondition: table is a String, with two possible values: "left", "right",
        corresponding to "TableA.csv" and "TableB.csv" respectively.
    """
    try:
        dataset = request.args.get('dataset')
        table = request.args.get('table')
        attributes = methods.getAttributes(table, dataset)
        response = app.response_class(
            response=attributes,
            mimetype='application/json'
        )
        return response
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        func_name = inspect.stack()[0][3] 
        response = app.response_class(
            response=json.dumps({'exception_type': str(exception_type), 'exception': str(e),
                                'func_name': str(func_name+'()'), 'filename': str(filename),    
                                'line_number': str(line_number)}),
            mimetype='application/json'
        )
        return response




@app.route("/requests/tupleIsProtected", methods=['POST'])
def tupleIsProtected():
    """
        Returns whether the tuple is protected

        The response is in JSON format.

        Parameter dataset: the dataset.
        Precondition: dataset is String.

        Parameter table: the table.
        Precondition: table is String, with two possible values: "left", "right"

        Parameter json: The attributes of the tuple.
        Precondition: json is a String in JSON format, containing all the
        values for every attribute of this tuple.
    """
    try:
        request_data = request.get_json()
        dataset = request_data['dataset']
        table = request_data['table']
        json_str = request_data['json']

        json_obj = json.loads(json_str)
        result = methods.checkTupleProtected(
            dataset, table, json_obj["attributes"])
        response = app.response_class(
            response=json.dumps({'is_protected': str(result)}),
            mimetype='application/json'
        )
        return response
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        func_name = inspect.stack()[0][3] 
        response = app.response_class(
            response=json.dumps({'exception_type': str(exception_type), 'exception': str(e),
                                'func_name': str(func_name+'()'), 'filename': str(filename),    
                                'line_number': str(line_number)}),
            mimetype='application/json'
        )
        return response



@app.route("/requests/pairIsProtected", methods=['POST'])
def getPairIsProtected():
    """
        Returns whether the pair is protected.

        The response is in JSON format.

        Parameter dataset: the dataset.
        Precondition: dataset is String.

        Parameter json1: The attributes of the left tuple.
        Precondition: json1 is a String in JSON format, containing all the
        values for every attribute of the left tuple.

        Parameter json2: The attributes of the right tuple.
        Precondition: json2 is a String in JSON format, containing all the
        values for every attribute of the left tuple.
    """
    try:
        request_data = request.get_json()
        dataset = request_data['dataset']
        json_str1 = request_data['json1']
        json_str2 = request_data['json2']

        json_obj1 = json.loads(json_str1)
        json_obj2 = json.loads(json_str2)
        result1 = methods.checkTupleProtected(dataset, 'right', json_obj1["right_table"])
        result2 = methods.checkTupleProtected(dataset, 'left', json_obj2["left_table"])
        pair_is_protected = result1 or result2

        response = app.response_class(
            response = json.dumps({'is_protected': str(pair_is_protected)}),
            mimetype = 'application/json'
        )
        return response
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        func_name = inspect.stack()[0][3] 
        response = app.response_class(
            response=json.dumps({'exception_type': str(exception_type), 'exception': str(e),
                                'func_name': str(func_name+'()'), 'filename': str(filename),    
                                'line_number': str(line_number)}),
            mimetype='application/json'
        )
        return response



@app.route("/requests/postProtectedCondition", methods=['POST'])
def postProtectedCondition():
    try:
        dataset_type = request.json['dataset_type']
        if dataset_type == "kg":
            dataset = request.json['dataset']
            min_size_thres = request.json['min_size_thres']
            operator = request.json['operator']
            condition = methods.construct_cond_kg(min_size_thres, operator)
            condition_w_exp = methods.construct_cond_kg(min_size_thres, operator)
        if dataset_type == "tab":
            dataset = request.json['dataset']
            left_attribute = request.json['left_attribute']
            left_func = request.json['left_func']
            left_value = request.json['left_value']
            logical_op = request.json['logical_op']
            right_attribute = request.json['right_attribute']
            right_func = request.json['right_func']
            right_value = request.json['right_value']
            condition = methods.construct_cond(left_attribute, left_func, left_value, logical_op, right_attribute, right_func, right_value, 0)
            condition_w_exp = methods.construct_cond(left_attribute, left_func, left_value, logical_op, right_attribute, right_func, right_value, 1)

        methods.saveNewCond(dataset, condition, condition_w_exp)
        methods.deleteCachedData(dataset)
        response = app.response_class(
            response = json.dumps({'status': 'succeed'}),
            mimetype = 'application/json'
        )
        return response
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        func_name = inspect.stack()[0][3] 
        response = app.response_class(
            response=json.dumps({'exception_type': str(exception_type), 'exception': str(e),
                                'func_name': str(func_name+'()'), 'filename': str(filename),    
                                'line_number': str(line_number)}),
            mimetype='application/json'
        )
        return response



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/requests/uploadDataset", methods=['POST'])
def uploadDataset():
    try:

        if 'dataset-upload-file' in request.files:
            dataset_type = "tab"
        if 'kg-upload-file' in request.files:
            dataset_type = "kg"

        # check if the post request has the file part
        if 'dataset-upload-file' not in request.files or 'kg-upload-file' not in request.files:
            response = app.response_class(
                response = json.dumps({'status': 'nofile'}),
                mimetype = 'application/json'
            )

        if dataset_type == "kg":
            file = request.files['kg-upload-file']
        elif dataset_type == "tab":
            file = request.files['dataset-upload-file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            response = app.response_class(
                response = json.dumps({'status': 'nofile'}),
                mimetype = 'application/json'
            )
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if methods.check_for_duplicates(filename):
                file.save(os.path.join(UPLOAD_DATASET_FOLDER, filename))
                methods.extract_dataset(filename)
                methods.delete_dataset_zip(filename)
                methods.read_uploaded_dataset(os.path.splitext(filename)[0], dataset_type)
                response = app.response_class(
                    response = json.dumps({'status': 'uploaded'}),
                    mimetype = 'application/json'
                )
            else:
                response = app.response_class(
                    response = json.dumps({'status': 'datasetexists'}),
                    mimetype = 'application/json'
                )
        else:
            response = app.response_class(
                response = json.dumps({'status': 'notallowed'}),
                mimetype = 'application/json'
            )
        
        return response

    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        func_name = inspect.stack()[0][3] 
        response = app.response_class(
            response=json.dumps({'exception_type': str(exception_type), 'exception': str(e),
                                'func_name': str(func_name+'()'), 'filename': str(filename),    
                                'line_number': str(line_number)}),
            mimetype='application/json'
        )
        return response



@app.route("/requests/getDatasetsNames", methods=['GET'])
def getDatasetsNames():
    """
        Returns a sorted list of names of all the datasets.

        The response is in JSON format.
    """
    try:
        data_names_json = methods.datasets_names_to_json()
        datasets_without_condition = methods.datasets_without_condition()
        non_cached_datasets = methods.non_cached_datasets()
        response = app.response_class(
            response = json.dumps({'datasets_list': sorted(data_names_json), 
                                    'datasets_without_condition': datasets_without_condition,
                                    'non_cached_datasets': non_cached_datasets
                                }),
            mimetype = 'application/json'
        )
        return response
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        func_name = inspect.stack()[0][3] 
        response = app.response_class(
            response=json.dumps({'exception_type': str(exception_type), 'exception': str(e),
                                'func_name': str(func_name+'()'), 'filename': str(filename),    
                                'line_number': str(line_number)}),
            mimetype='application/json'
        )
        return response


@app.route("/requests/downloadDMdatasets", methods=['POST'])
def downloadDMdatasets():
    """
        Downloads and sets up all the datasets from Deepmatcher.
        (https://github.com/anhaidgroup/deepmatcher/blob/master/Datasets.md)

        The response is in JSON format.
    """
    try:
        
        methods.download_dm_dataset()
        methods.read_dm_datasets()
        response = app.response_class(
            response = json.dumps({'status': 'succeed'}),
            mimetype = 'application/json'
        )
        return response
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        func_name = inspect.stack()[0][3] 
        response = app.response_class(
            response=json.dumps({'exception_type': str(exception_type), 'exception': str(e),
                                'func_name': str(func_name+'()'), 'filename': str(filename),    
                                'line_number': str(line_number)}),
            mimetype='application/json'
        )
        return response

@app.route("/requests/downloadKGdatasets", methods=['POST'])
def downloadKGdatasets():
    """
        Downloads and sets up all the datasets from ...
        (link for datasets)

        The response is in JSON format.
    """
    try:
        methods.download_kg_dataset()
        methods.read_kg_datasets()
        response = app.response_class(
            response = json.dumps({'status': 'succeed'}),
            mimetype = 'application/json'
        )
        return response
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        func_name = inspect.stack()[0][3] 
        response = app.response_class(
            response=json.dumps({'exception_type': str(exception_type), 'exception': str(e),
                                'func_name': str(func_name+'()'), 'filename': str(filename),    
                                'line_number': str(line_number)}),
            mimetype='application/json'
        )
        return response

@app.route("/requests/tupleIsProtectedJSON", methods=['POST'])
def tupleIsProtectedJSON():
    """
        Returns whether the tuple is protected.

        The response is in JSON format.

        Parameter json-upload-file: the file that the user uploaded.
        Precondition: json-upload-file is File(.json), containing all the
        values for every attribute of this tuple.

        Parameter dataset: the dataset.
        Precondition: dataset is String.

        Parameter table: the table.
        Precondition: table is String, with two possible values: "left", "right"
    """
    try:
        # check if the post request has the file part
        if 'json-upload-file' not in request.files:
            response = app.response_class(
                response = json.dumps({'status': 'nofile'}),
                mimetype = 'application/json'
            )
            return response
        file = request.files['json-upload-file']
        dataset = request.form["dataset"]
        table = request.form["table"]

        if file.filename == '':
            response = app.response_class(
                response = json.dumps({'status': 'nofile'}),
                mimetype = 'application/json'
            )
            return response

        if file and allowed_file(file.filename):
            contents = file.read()
            json_obj = json.loads(contents)

            result = methods.checkTupleProtected(dataset, table, json_obj["attributes"])  
            response = app.response_class(
                response = json.dumps({'status': str(result)}),
                mimetype = 'application/json'
            )
        else:
            response = app.response_class(
                response = json.dumps({'status': 'notallowed'}),
                mimetype = 'application/json'
            )
        
        return response
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        func_name = inspect.stack()[0][3] 
        response = app.response_class(
            response=json.dumps({'exception_type': str(exception_type), 'exception': str(e),
                                'func_name': str(func_name+'()'), 'filename': str(filename),    
                                'line_number': str(line_number)}),
            mimetype='application/json'
        )
        return response


@app.route("/requests/pairIsProtectedJSON", methods=['POST'])
def pairIsProtectedJSON():
    """
            Returns whether the pair is protected.

            The response is in JSON format.

            Parameter dataset: the dataset.
            Precondition: dataset is String.

            Parameter json-upload-file: The attributes of the left tuple.
            Precondition: json-upload-file is File(.json), containing all the
            values for every attribute of the pair (left and right tuple).
    """
    try:
        # check if the post request has the file part
        if 'json-upload-file' not in request.files:
            response = app.response_class(
                response = json.dumps({'status': 'nofile'}),
                mimetype = 'application/json'
            )
            return response
        file = request.files['json-upload-file']
        dataset = request.form["dataset"]
        

        if file.filename == '':
            response = app.response_class(
                response = json.dumps({'status': 'nofile'}),
                mimetype = 'application/json'
            )
            return response
            
        if file and allowed_file(file.filename):
            contents = file.read()
            json_obj = (json.loads(contents))["tables"]
            result1 = methods.checkTupleProtected(dataset, 'right', json_obj[1].get("right"))
            result2 = methods.checkTupleProtected(dataset, 'left', json_obj[0].get("left"))

            pair_is_protected = result1 or result2  
            response = app.response_class( 
                response = json.dumps({'status': str(pair_is_protected)}), 
                mimetype = 'application/json'
            )
        else:
            response = app.response_class(
                response = json.dumps({'status': 'notallowed'}),
                mimetype = 'application/json'
            )
        
        return response
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        func_name = inspect.stack()[0][3] 
        response = app.response_class(
            response=json.dumps({'exception_type': str(exception_type), 'exception': str(e),
                                'func_name': str(func_name+'()'), 'filename': str(filename),    
                                'line_number': str(line_number)}),
            mimetype='application/json'
        )
        return response


@app.route("/requests/getExplanation", methods=['GET'])
def getExplanation():
    """
        Returns the explanation figures (two base64 images).

        The response is in JSON format.

        Parameter dataset: the dataset.
        Precondition: dataset is String.
    """

    try:
        dataset = request.args.get('dataset')
        method = request.args.get('method')
        if method == "deepmatcher":
            if methods.explanation_exists(dataset):
                methods.deleteCachedData(dataset)
                methods.runFairER(dataset, 1)
                base64_1 = methods.img_to_base64(dataset, 'Figure_1.png')
                base64_2 = methods.img_to_base64(dataset, 'Figure_2.png')
                response = app.response_class(
                        response = json.dumps({'base64_1': base64_1, 'base64_2': base64_2}),
                        mimetype = 'application/json'
                    )
                
                return response
        else:
            # dataset = request.args.get('dataset')
            alg = request.args.get('alg')
            explanation = request.args.get('explanation')
            p = request.args.get('p')
            s = request.args.get('s')
            t = request.args.get('t')
            print(request.args)
            if p == None:
                conf = "original"
            else:
                conf = p + "_" + s + "_" + t
            
            if method == "deepmatcher":
                if alg == 'fairER':
                    methods.runFairER(dataset, explanation)  
                else:
                    methods.runUnfair(dataset) 
            elif method == "RREA" or method == "BERT_INT":
                if alg == 'fairER':
                        methods.runFairER_RREA(dataset, explanation, conf, method=method)
                else:
                        methods.runUnfair_RREA(dataset, explanation, conf, method=method)
            elif method == "RDGCN" or method == "MultiKE" or method == "PARIS":
                if alg == 'fairER':
                        methods.runFairER_OpenEA(dataset, explanation, conf, method)
                else:
                        methods.runUnfair_OpenEA(dataset, explanation, conf, method)

            with open(os.path.join(os.getcwd() + '/web/' + 'data', 'json_data', 'clusters_data.json')) as json_file:
                data = json.load(json_file)

            response = app.response_class(
                response=json.dumps({'clusters': str(data["clusters"]), 'candidates': str(data["candidates"])}),
                mimetype='application/json'
            )
                
            return response
        
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        func_name = inspect.stack()[0][3] 
        response = app.response_class(
            response=json.dumps({'exception_type': str(exception_type), 'exception': str(e),
                                'func_name': str(func_name+'()'), 'filename': str(filename),    
                                'line_number': str(line_number)}),
            mimetype='application/json'
        )
        return response

@app.route("/requests/deleteDataset", methods=['DELETE'])
def deleteDataset():
    try:
        dataset = request.args.get('dataset')   
        status = methods.delete_dataset(dataset)
        response = app.response_class(
                response = json.dumps({'status': str(status)}),
                mimetype = 'application/json'
        )
        return response
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        func_name = inspect.stack()[0][3] 
        response = app.response_class(
            response=json.dumps({'exception_type': str(exception_type), 'exception': str(e),
                                'func_name': str(func_name+'()'), 'filename': str(filename),    
                                'line_number': str(line_number)}),
            mimetype='application/json'
        )
        return response


@app.route('/requests/runSampling', methods=['GET'])
def startSampling():
    """
        ...
    """
    try:
        
        dataset = request.args.get('dataset')
        method = request.args.get('method')
        p = request.args.get('p')
        s = request.args.get('s')
        t = request.args.get('t')
        resp = methods.run_sampling(dataset, method, p, s, t)
        response = app.response_class(
            response=json.dumps({'message': resp}),
            mimetype='application/json'
        )
        return response
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        func_name = inspect.stack()[0][3] 
        response = app.response_class(
            response=json.dumps({'exception_type': str(exception_type), 'exception': str(e),
                                'func_name': str(func_name+'()'), 'filename': str(filename),    
                                'line_number': str(line_number)}),
            mimetype='application/json'
        )
        return response
    


if __name__ == "__main__":
    app.run(debug=False, threaded=True, port=5052)