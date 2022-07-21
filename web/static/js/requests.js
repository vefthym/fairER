function delete_dataset(dataset) {
    $.ajax({
        type: 'DELETE',
        url: "/requests/deleteDataset?dataset=" + dataset,
        contentType: "application/json",
        dataType: 'text',
        success: function (response) {
            var obj = response;
            //If there is no exception 
            if (obj.exception == undefined) {
                pretty_alert('success', 'Done!', '<b>"' + dataset + '"</b> has been deleted successfully!')
                
                setTimeout(function () { location.reload(); }, 2600);
            }
                
            //If there is an exception, print details about it
            else print_exception(obj.exception_type, obj.exception, obj.filename, obj.func_name, obj.line_number)
        },
        error: function (error) {
            console.log(error);
        }
    });
}

function post_protected_condition() {
    left_attribute = $("#left-tpl").val();
    left_func = $("#left-func-select").val();
    left_value = $("#left-value").val();
    logical_op = $("#logical-op-select").val();
    right_attribute = $("#right-tpl").val();
    right_func = $("#right-func-select").val();
    right_value = $("#right-value").val();

    var dataset = $('#dataset-val').val();
    $.ajax({
        url: '/requests/postProtectedCondition',
        type: 'POST',
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({
            'dataset': dataset,
            'left_attribute': left_attribute,
            'left_func': left_func,
            'left_value': left_value,
            'logical_op': logical_op,
            'right_attribute': right_attribute,
            'right_func': right_func,
            'right_value': right_value
        }),
        success: function (response) {
            var obj = response;
            //If there is no exception 
            if (obj.exception == undefined) {
                Swal.fire({
                    position: 'center',
                    icon: 'success',
                    title: 'Done!',
                    text: 'Protected Condition has been changed successfully!',
                    showConfirmButton: false,
                    timer: 3200
                })
                if(datasets_without_condition.includes(dataset))
                    datasets_without_condition.splice(datasets_without_condition.indexOf(dataset));
                non_cached_datasets.push(dataset);
                clear_all_containers();
            }
            //If there is an exception, print details about it
            else print_exception(obj.exception_type, obj.exception, obj.filename, obj.func_name, obj.line_number)
        },
        error: function (error) {
            console.log(error);
        }
    });
}
/* If the parameter is undefined, it just returns the protected condition,
    otherwise it prints it in the 'container_id' html element*/
function get_condition(container_id) {
    var dataset = $('#dataset-val').val();
    $.ajax({
        type: "GET",
        url: "/requests/getProtectedCondition?dataset=" + dataset,
        contentType: "application/json",
        dataType: 'text',
        success: function (response) {
            var obj = JSON.parse(response);
            //If there is no exception 
            if (obj.exception == undefined) {
                if (container_id != null) {
                    let hrmlRes = '<label for="condition" class="form-label"><b>Current Condition:</b></label>'
                    hrmlRes += '<p id="condition">&emsp;' + obj.condition + '</p>'
                    $('#' + container_id).html(hrmlRes)
                }
                else {

                    return obj.condition;
                }
            }
            //If there is an exception, print details about it
            else print_exception(obj.exception_type, obj.exception, obj.filename, obj.func_name, obj.line_number)
        },
        error: function (error) {
            console.log(error);
            return error;
        }
    });
}


/* Returns the attributes of a specific dataset's table ('right' or 'left') */
function get_attributes(table) {
    var dataset = $('#dataset-val').val()

    $.ajax({
        type: "GET",
        url: "/requests/getTableAttributes?dataset=" + dataset + "&table=" + table,
        contentType: "application/json",
        dataType: 'text',
        success: function (response) {
            var obj = JSON.parse(response);
            //If there is no exception 
            if (obj.exception == undefined) {
                tuple_attributes_to_input(obj, table);
            }
            //If there is an exception, print details about it
            else print_exception(obj.exception_type, obj.exception, obj.filename, obj.func_name, obj.line_number)
        },
        error: function (error) {
            console.log(error);
        }
    });
}

/* Sends the uploaded JSON file to the server and returns whether the tuple is protected */
function tuple_is_protected_JSON(table) {

    if (has_condition() == false)
        return;

    var dataset = $('#dataset-val').val()

    var form_data = new FormData($('#json-upload-form')[0]);
    if (form_data.get("json-upload-file")["name"].length == 0) {
        pretty_alert('error', 'Error!', 'You did not select a JSON!')
        return;
    }
    form_data.append('dataset', dataset)
    form_data.append('table', table)
    $.ajax({
        type: 'POST',
        url: '/requests/tupleIsProtectedJSON',
        processData: false,
        contentType: false,
        async: false,
        cache: false,
        data: form_data,
        success: function (data) {
            //If there is no exception 
            if (data.exception == undefined) {
                if (data.status == 'nofile')
                    pretty_alert('error', 'Error!', 'You did not select a dataset to upload!')

                else if (data.status == 'datasetexists')
                    pretty_alert('error', 'Error!', 'A duplicate dataset\'s name found on the system!')
                else if (data.status == 'notallowed')
                    pretty_alert('error', 'Error!', 'Dataset\s file extention should be .zip!')
                else {
                    if (data.status == 'True')
                        $('#protected-container').html('<b>Tuple is protected!</b>');
                    else
                        $('#protected-container').html('<b>Tuple is not protected!</b>');
                }
            }
            //If there is an exception, print details about it
            else print_exception(data.exception_type, data.exception, data.filename, data.func_name, data.line_number)
        }
    });
}



/* Sends the uploaded JSON file to the server and returns whether the pair is protected */
function pair_is_protected_JSON() {

    if (has_condition() == false)
        return;

    var dataset = $('#dataset-val').val()

    var form_data = new FormData($('#json-upload-form')[0]);
    if (form_data.get("json-upload-file")["name"].length == 0) {
        pretty_alert('error', 'Error!', 'You did not select a JSON!')
        return;
    }
    form_data.append('dataset', dataset)
    $.ajax({
        type: 'POST',
        url: '/requests/pairIsProtectedJSON',
        processData: false,
        contentType: false,
        async: false,
        cache: false,
        data: form_data,
        success: function (data) {
            //If there is no exception 
            if (data.exception == undefined) {
                if (data.res == 'nofile')
                    pretty_alert('error', 'Error!', 'You did not select a dataset to upload!')

                else if (data.status == 'datasetexists')
                    pretty_alert('error', 'Error!', 'A duplicate dataset\'s name found on the system!')

                else if (data.status == 'notallowed')
                    pretty_alert('error', 'Error!', 'Dataset\s file extention should be .zip!')
                else {
                    if (data.status == 'True')
                        $('#protected-container').html('<b>Pair is protected!</b>');
                    else
                        $('#protected-container').html('<b>Pair is not protected!</b>');
                }
            }
            //If there is an exception, print details about it
            else print_exception(data.exception_type, data.exception, data.filename, data.func_name, data.line_number)
        }
    });
}


/* Prints whether a tuple is protected */
function tuple_is_protected(table) {

    if (has_condition() == false)
        return;

    var dataset = $('#dataset-val').val()
    var json_str = '{ "attributes" : [';

    $("form#attr-form :input").each(function () {
        json_str += '{ "' + $(this).attr('id') + '": "' + $(this).val() + '" },';
    });
    json_str = json_str.slice(0, -1); //remove the last comma
    json_str += ' ]}';

    $.ajax({
        type: "POST",
        url: '/requests/tupleIsProtected',
        contentType: 'application/json',
        data: JSON.stringify({ "dataset": dataset, table: table, json: json_str }),
        success: (data) => {
            //If there is no exception 
            if (data.exception == undefined) {
                if (data.is_protected == 'True')
                    $('#protected-container').html('<b>Tuple is protected!</b>');
                else
                    $('#protected-container').html('<b>Tuple is not protected!</b>');
            }
            //If there is an exception, print details about it
            else print_exception(data.exception_type, data.exception, data.filename, data.func_name, data.line_number)
        },
        error: function (error) {
            console.log(error);
        }
    });
}



/* Returns and prints the attributes of the pair as inputs to the user */
function get_pair_fields() {

    if (has_condition() == false)
        return;

    var dataset = $('#dataset-val').val();

    $.ajax({
        type: "GET",
        url: "/requests/getTableAttributes?dataset=" + dataset + "&table=right",
        contentType: "application/json",
        dataType: 'text',
        success: function (response) {
            var right_obj = JSON.parse(response);
            //If there is no exception 
            if (right_obj.exception == undefined) {
                $.ajax({
                    type: "GET",
                    url: "/requests/getTableAttributes?dataset=" + dataset + "&table=left",
                    contentType: "application/json",
                    dataType: 'text',
                    success: function (response) {
                        var left_obj = JSON.parse(response);
                        //If there is no exception 
                        if (left_obj.exception == undefined)
                            pair_attributes_to_input(right_obj, left_obj);
                        //If there is an exception, print details about it
                        else print_exception(left_obj.exception_type, left_obj.exception, left_obj.filename, left_obj.func_name, left_obj.line_number)
                    },
                    error: function (error) {
                        console.log(error);
                    }
                });
            }
            //If there is an exception, print details about it
            else print_exception(right_obj.exception_type, right_obj.exception, right_obj.filename, right_obj.func_name, right_obj.line_number)

        },
        error: function (error) {
            console.log(error);
        }
    });
}

/* Prints whether a tuple is protected */
function pair_is_protected() {
    if (has_condition() == false)
        return;

    var dataset = $('#dataset-val').val()

    //Build a json with all the data from the form
    var str1 = '{ "right_table" : [';

    $("form#attr-form :input").each(function () {
        if ($(this).attr('id') && attr_prefix($(this).attr('id')) == 'right')
            str1 += '{ "' + clear_prefix($(this).attr('id')) + '": "' + $(this).val() + '" },';
    });
    str1 = str1.slice(0, -1); //remove the last comma
    str1 += ' ]}';

    var str2 = '{ "left_table" : [';

    $("form#attr-form :input").each(function () {
        if ($(this).attr('id') && attr_prefix($(this).attr('id')) == 'left')
            str2 += '{ "' + clear_prefix($(this).attr('id')) + '": "' + $(this).val() + '" },';
    });
    str2 = str2.slice(0, -1); //remove the last comma
    str2 += ' ]}';


    $.ajax({
        type: "POST",
        url: '/requests/pairIsProtected',
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify({ 'dataset': dataset, 'json1': str1, 'json2': str2 }),
        success: function (data) {
            //If there is no exception 
            if (data.exception == undefined) {
                if (data.is_protected == 'True')
                    $('#protected-container').html('<b>Pair is protected!</b>');
                else
                    $('#protected-container').html('<b>Pair is not protected!</b>');
            }
            //If there is an exception, print details about it
            else print_exception(data.exception_type, data.exception, data.filename, data.func_name, data.line_number)
        },
        error: function (error) {
            console.log(error);
        }
    });
}

/* Prints the predictions in the 'container_id' html element */
function get_predictions(alg, container_id) {
    var explanation = 1;
    var dataset = $('#dataset-val').val()
    if (has_condition() == false)
        return;


    if (non_cached_datasets.includes(dataset)){
        if(document.querySelector('input[name="exp-form"]:checked') == null){
            has_cached_data();
            return;
        }
        explanation = parseInt(document.querySelector('input[name="exp-form"]:checked').value);
        document.getElementById('datasets-info-container').innerHTML = "";
    }

    $('#' + container_id).html('<div class="loader"></div><p style="text-align:center; margin-top:1%">Please wait as this may take a few minutes...</p>')
    
    $.ajax({
        type: "GET",
        url: "/requests/getPreds?alg=" + alg + "&dataset=" + dataset + "&explanation=" + explanation,
        contentType: "application/json",
        dataType: 'text',
        success: function (response) {
            var obj = JSON.parse(response);
            //If there is no exception 
            if (obj.exception == undefined) {
                var pred_data = eval(obj.preds);


                if (alg == "unfair")
                    $('#unfair-container').html('<label for="predictions-table">Predictions</label><div id="predictions-table-' + container_id + '"></div>');
                else
                    $('#fairer-container').html('<label for="predictions-table">Predictions</label><div id="predictions-table-' + container_id + '"></div>');

                $('#predictions-table-' + container_id).addClass("table-bordered responsive-table striped");

                var table = new Tabulator("#predictions-table-" + container_id, {
                    data: pred_data,           //load row data from array
                    layout: "fitColumns",      //fit columns to width of table
                    responsiveLayout: "hide",  //hide columns that dont fit on the table
                    addRowPos: "top",          //when adding a new row, add it to the top of the table
                    pagination: "local",       //paginate the data
                    paginationSize: 15,         //allow 15 rows per page of data
                    paginationCounter: "rows", //display count of paginated rows in footer
                    autoColumns: true,
                });
                if(non_cached_datasets.includes(dataset))
                    remove_from_noncached_datasets(dataset);
            }
            //If there is an exception, print details about it
            else print_exception(obj.exception_type, obj.exception, obj.filename, obj.func_name, obj.line_number)
        },
        error: function (error) {
            console.log(error);
        }
    });
}


/* Prints the clusters in the 'container_id' html element */
function get_clusters(alg, container_id) {
    var explanation = 1;
    var dataset = $('#dataset-val').val()
    if (has_condition() == false)
        return;


    if (non_cached_datasets.includes(dataset)){
        if(document.querySelector('input[name="exp-form"]:checked') == null){
            has_cached_data();
            return;
        }
        explanation = parseInt(document.querySelector('input[name="exp-form"]:checked').value);
        document.getElementById('datasets-info-container').innerHTML = "";
    }

    $('#' + container_id).html('<div class="loader"></div><p style="text-align:center; margin-top:1%">Please wait as this may take a few minutes...</p>')

    $.ajax({
        type: "GET",
        url: "/requests/getClusters?alg=" + alg + "&dataset=" + dataset + "&explanation=" + explanation,
        contentType: "application/json",
        dataType: 'text',
        success: function (response) {
            var obj = JSON.parse(response);
            //If there is no exception 
            if (obj.exception == undefined) {
                var clusters_data = eval(obj.clusters);
                if (alg == "unfair")
                    $('#unfair-container').html('<label for="clusters-table" id="clusters-label">Clusters</label><div id="clusters-table-' + container_id + '"></div>');
                else
                    $('#fairer-container').html('<label for="clusters-table" id="clusters-label">Clusters</label><div id="clusters-table-' + container_id + '"></div>');
                $('#clusters-table' + container_id).addClass("table-bordered responsive-table");
                var table = new Tabulator("#clusters-table-" + container_id, {
                    data: clusters_data,           //load row data from array
                    layout: "fitColumns",      //fit columns to width of table
                    responsiveLayout: "hide",  //hide columns that dont fit on the table
                    addRowPos: "top",          //when adding a new row, add it to the top of the table
                    pagination: "local",       //paginate the data
                    paginationSize: 15,         //allow 15 rows per page of data
                    autoColumns: true,
                });
                if(non_cached_datasets.includes(dataset))
                    remove_from_noncached_datasets(dataset);
            }
            //If there is an exception, print details about it
            else print_exception(obj.exception_type, obj.exception, obj.filename, obj.func_name, obj.line_number)

        },
        error: function (error) {
            console.log(error);
        }
    });
}


/* Prints the evaluation results in the 'container_id' html element */
function get_evaluation(alg, container_id) {
    var explanation = 1;
    var dataset = $('#dataset-val').val()
    if (has_condition() == false)
        return;


    if (non_cached_datasets.includes(dataset)){
        if(document.querySelector('input[name="exp-form"]:checked') == null){
            has_cached_data();
            return;
        }
        explanation = parseInt(document.querySelector('input[name="exp-form"]:checked').value);
        document.getElementById('datasets-info-container').innerHTML = "";
    }

    $('#' + container_id).html('<div class="loader"></div><p style="text-align:center; margin-top:1%">Please wait as this may take a few minutes...</p>')

    $.ajax({
        type: "GET",
        url: "/requests/getEvaluationResults?alg=" + alg + "&dataset=" + dataset + "&explanation=" + explanation,
        contentType: "application/json",
        dataType: 'text',
        success: function (response) {
            const obj = JSON.parse(response);
            //If there is exception 
            if (obj.exception == undefined) {
                $('#' + container_id).html('<label for="eval-table" id="eval-label">Evaluation Results</label><div id="eval-table-' + container_id + '"></div>');
                $('#eval-table-' + container_id).addClass("table-bordered responsive-table");

                data = '[' + response + ']'
                data = JSON.parse(JSON.parse(JSON.stringify(data)));
                var table = new Tabulator("#eval-table-" + container_id, {
                    data: data,           //load row data from array
                    layout: "fitColumns",      //fit columns to width of table
                    responsiveLayout: "hide",  //hide columns that dont fit on the table
                    autoColumns: true,
                });
                eval_res_description(container_id);
                if(non_cached_datasets.includes(dataset))
                    remove_from_noncached_datasets(dataset);
            }
            //If there is an exception, print details about it
            else print_exception(obj.exception_type, obj.exception, obj.filename, obj.func_name, obj.line_number)
        },
        error: function (error) {
            console.log(error);
        }
    });
}



/* Prints the statistics */
function get_statistics() {
    var explanation = 1
    
    if (has_condition() == false)
        return;

    $('#datasets-info-container').html('<div class="loader"></div><p style="text-align:center; margin-top:1%">Please wait as this may take a few minutes...</p>')
    var dataset = $('#dataset-val').val()

    if (non_cached_datasets.includes(dataset)){
        if(document.querySelector('input[name="exp-form"]:checked') == null){
            has_cached_data();
            return;
        }
        explanation = parseInt(document.querySelector('input[name="exp-form"]:checked').value);
        document.getElementById('datasets-info-container').innerHTML = "";
    }

    $.ajax({
        type: "GET",
        url: "/requests/getStatistics?dataset=" + dataset + "&explanation=" + explanation,
        contentType: "application/json",
        dataType: 'text',
        success: function (response) {
            const obj = JSON.parse(response);
            //If there is no exception 
            if (obj.exception == undefined) {

                $('#datasets-info-container').html('<label for="statistics-table">Statistics</label><div id="statistics-table"></div>');
                $('#statistics-table').addClass("table-bordered responsive-table");

                data = '[' + response + ']'
                data = JSON.parse(JSON.parse(JSON.stringify(data)));
                console.log(data)
                var table = new Tabulator("#statistics-table", {
                    data: data,           //load row data from array
                    layout: "fitColumns",      //fit columns to width of table
                    responsiveLayout: "hide",  //hide columns that dont fit on the table
                    autoColumns: true,
                });
                if(non_cached_datasets.includes(dataset))
                    remove_from_noncached_datasets(dataset);

            }
            //If there is an exception, print details about it
            else print_exception(obj.exception_type, obj.exception, obj.filename, obj.func_name, obj.line_number)
        },
        error: function (error) {
            console.log(error);
        }
    });
}

function upload_dataset() {
    var form_data = new FormData($('#dataset-upload-form')[0]);
    if (form_data.get("dataset-upload-file")["name"].length == 0) {
        pretty_alert('error', 'Error!', 'You did not select a dataset to upload!')
        return;
    }
    $.ajax({
        type: 'POST',
        url: '/requests/uploadDataset',
        processData: false,
        contentType: false,
        async: false,
        cache: false,
        data: form_data,
        success: function (data) {
            //If there is no exception 
            if (data.exception == undefined) {
                if (data.status == 'uploaded'){
                    pretty_alert('success', 'Done!', 'Dataset has been uploaded successfully!')

                    let dataset_name = form_data.get("dataset-upload-file")["name"].slice(0, -4);
                    var option = document.createElement("option");
                    option.value = dataset_name;
                    option.text = dataset_name;
                    document.getElementById('dataset-val').appendChild(option);

                    document.getElementById('dataset-val').value = dataset_name;
                    clear_all_containers();
                    non_cached_datasets.push(dataset_name);
                    datasets_without_condition.push(dataset_name);
                    has_cached_data();
                }
                    

                else if (data.status == 'nofile')
                    pretty_alert('error', 'Error!', 'You did not select a dataset to upload!')

                else if (data.status == 'datasetexists'){
                    pretty_alert('error', 'Error!', 'A duplicate dataset\'s name found on the system!')
                    setTimeout(function () { location.reload(); }, 3000);
                }

                else{
                    pretty_alert('error', 'Error!', 'Dataset\s file extention should be .zip!')
                    setTimeout(function () { location.reload(); }, 3000);
                }
                    
            }
            //If there is an exception, print details about it
            else print_exception(data.exception_type, data.exception, data.filename, data.func_name, data.line_number)
        }
    });
}

/* (on-page-load) Checks for the available datasets and fills the dataset selection dropdown.
    If there is no available datasets, it shows an option to download the Deepmatcher datasets. */
    $(document).ready(function () {
        $.ajax({
            type: "GET",
            url: "/requests/getDatasetsNames",
            success: function (response) {
                //If there is no exception 
                if (response.exception == undefined) {
                    datasets_names_list = response.datasets_list
                    non_cached_datasets = response.non_cached_datasets
                    datasets_without_condition = response.datasets_without_condition
                    if (datasets_names_list.length == 0) {
                        $("#select-dataset-label").html("")
                        $("#datasets-container").css("display", "block");
                        $("#datasets-container").css("text-align", "center");
                        htmlRes = '<p style="color:red">No datasets found on system!</p>' +
                            '<b><p>Press the button to download the Datasets from DeepMatcher.</b></p>' +
                            '<button type="button" class="btn btn-success" onclick="download_dm_datasets()">Download</button>';
                        $('#datasets-container').html(htmlRes)
                    }
                    else {
                        var data = [];
                        datasets_names_list.forEach(item =>
                            data.push({ id: item, text: item })
                        );
                        $('#datasets-container').html('<select id="dataset-val" style="width:80%;" onchange="has_cached_data()"></select>')
    
                        let statistics_btn = document.createElement("button");
                        statistics_btn.innerHTML = "Dataset Statistics";
                        statistics_btn.className = "btn btn-secondary";
                        statistics_btn.addEventListener("click", function () {
                            get_statistics();
                        });
                        $("#datasets-container").append(statistics_btn)

                        let upload_btn = document.createElement("button");
                        upload_btn.innerHTML = "Upload Dataset";
                        upload_btn.className = "btn btn-secondary";
                        upload_btn.addEventListener("click", function () {
                            clear_all_containers();
                            upload_dataset_info();
                        });
                        $("#datasets-container").append(upload_btn)

                        let delete_btn = document.createElement("button");
                        delete_btn.innerHTML = "Delete Dataset";
                        delete_btn.className = "btn btn-danger";
                        delete_btn.addEventListener("click", function () {
                            delete_dataset_message();
                        });
                        $("#datasets-container").append(delete_btn)


    
                        $("#dataset-val").select2({
                            data: data
                        })
                        has_cached_data();
                    }
                }
                //If there is an exception, print details about it
                else print_exception(response.exception_type, response.exception, response.filename, response.func_name, response.line_number)
            },
            error: function (error) {
                console.log(error);
            }
        });
    });


/* Downloads Deepmatcher datasets */
function download_dm_datasets() {
    htmlRes = '<b><p>Datasets are dowloading.</b></p><p>Estimated time: 30sec.</p>' +
        '<div class="loader"></div>';
    $('#datasets-container').html(htmlRes)
    $.ajax({
        url: '/requests/downloadDMdatasets',
        type: 'POST',
        success: function (response) {
            //If there is no exception 
            if (response.exception == undefined) {
                $('#datasets-container').html('')
                Swal.fire({
                    position: 'center',
                    icon: 'success',
                    title: 'Done!',
                    text: 'The page will be reloaded.',
                    showConfirmButton: false,
                    timer: 3000
                })
                setTimeout(function () { location.reload(); }, 3000);
            }
            //If there is an exception, print details about it
            else print_exception(response.exception_type, response.exception, response.filename, response.func_name, response.line_number)
        },
        error: function (error) {
            console.log(error);
        }
    });
}



/* Prints explanations */
function get_explanation() {
    $('#fairer-container').html('<div class="loader"></div><p style="text-align:center; margin-top:1%">Please wait as this may take a few minutes...</p>')
    var dataset = $('#dataset-val').val()

    if (non_cached_datasets.includes(dataset))
        document.getElementById('datasets-info-container').innerHTML = "";

    $.ajax({
        type: "GET",
        url: "/requests/getExplanation?dataset=" + dataset,
        dataType: 'text',
        success: function (response) {
            const obj = JSON.parse(response);
            //If there is no exception 
            if (obj.exception == undefined) {

                let galery_html = '<div>'
                    + '<ul id="images">'
                    + '<li id="first-expl-img"></li>'
                    + '<li id="second-expl-img"></li>'
                    + '</ul>'
                    + '</div>'


                let image1 = new Image();
                image1.src = 'data:image/png;base64,' + obj.base64_1;
                image1.alt = 'Figure 1'
                image1.id = 'img1'

                let image2 = new Image();
                image2.src = 'data:image/png;base64,' + obj.base64_2;
                image2.alt = 'Figure 2'
                image2.id = 'img2'


                $('#fairer-container').html(galery_html);
                $('#first-expl-img').html(image1);
                $('#second-expl-img').html(image2);
                $('#images').hide();
                let gallery = new Viewer(document.getElementById('images'));
                gallery.show();
                if(non_cached_datasets.includes(dataset))
                    remove_from_noncached_datasets(dataset);
            }
            //If there is an exception, print details about it
            else print_exception(obj.exception_type, obj.exception, obj.filename, obj.func_name, obj.line_number)
        },
        error: function (error) {
            console.log(error);
        }
    });
}