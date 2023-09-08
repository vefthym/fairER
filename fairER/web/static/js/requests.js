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
   
    var dataset = $('#dataset-val').val();
    var dataset_type = $('#dataset-val').select2("data")[0].type
    if(dataset_type == "kg"){
        min_size_thres = $("#slider-input").val();
        operator = $("#logical-op-select").val();
        obj = {
            'dataset': dataset,
            'dataset_type': dataset_type,
            'min_size_thres': min_size_thres,
            'operator': operator,
        }
    }else if(dataset_type == "tab"){
        left_attribute = $("#left-tpl").val();
        left_func = $("#left-func-select").val();
        left_value = $("#left-value").val();
        logical_op = $("#logical-op-select").val();
        right_attribute = $("#right-tpl").val();
        right_func = $("#right-func-select").val();
        right_value = $("#right-value").val();
        obj = {
            'dataset': dataset,
            'dataset_type': dataset_type,
            'left_attribute': left_attribute,
            'left_func': left_func,
            'left_value': left_value,
            'logical_op': logical_op,
            'right_attribute': right_attribute,
            'right_func': right_func,
            'right_value': right_value
        }
    }

    $.ajax({
        url: '/requests/postProtectedCondition',
        type: 'POST',
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(obj),
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
                get_condition('protected-container');
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
function get_condition(container_id, callback) {
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
                    callback(obj.condition);
                }
            }
            //If there is an exception, print details about it
            else print_exception(obj.exception_type, obj.exception, obj.filename, obj.func_name, obj.line_number)
        },
        error: function (error) {
            console.log(error);
            callback(null, error);
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
function get_predictions(alg, container_id, method, conf) {
    var explanation = 0;
    var dataset = $('#dataset-val').val()

    // if (conf == "original"){
    //     url = "/requests/getPreds?alg=" + alg + "&dataset=" + dataset + "&method=" + method + "&explanation=" + explanation;
    // }
    // else {
    //     url = "/requests/getPreds?alg=" + alg + "&dataset=" + dataset + "&method=" + method + "&explanation=" + explanation + conf;
    // }

    url = "/requests/getPreds?alg=" + alg + "&dataset=" + dataset + "&method=" + method + "&explanation=" + explanation;

    if (has_condition() == false)
        return;

    var dataset_type = $('#dataset-val').select2("data")[0].type

    if (non_cached_datasets.includes(dataset)){
        if(dataset_type == "tab" && document.querySelector('input[name="exp-form"]:checked') == null){
            has_cached_data();
            return;
        }
        if(dataset_type == "tab"){
            explanation = parseInt(document.querySelector('input[name="exp-form"]:checked').value);
        }
        document.getElementById('datasets-info-container').innerHTML = "";
    }

    $('#' + container_id).html('<div class="loader"></div><p style="text-align:center; margin-top:1%">Please wait as this may take a few minutes...</p>')
    
    $.ajax({
        type: "GET",
        url: url,
        contentType: "application/json",
        dataType: 'text',
        async: false,
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

function run_sampling(p, s, t) {

    var dataset = $('#dataset-val').val()
    var method = $('#method-val').val()
    // var p = $('#jump_prob').val()
    // var s = $('#sampl_size').val()
    // var t = $('#min_comp').val()

    if(!validation_hyper()){
        return
    }

    $.ajax({
        type: "GET",
        url: "/requests/runSampling?dataset=" + dataset + "&method=" + method + "&p=" + p + "&s=" + s + "&t=" + t,
        dataType: 'text',
        async: false,
        success: function (response) {
            const obj = JSON.parse(response);
            //If there is no exception 
            if (obj.exception == undefined) {
                console.log(obj.message)
            }
            //If there is an exception, print details about it
            else print_exception(obj.exception_type, obj.exception, obj.filename, obj.func_name, obj.line_number)
        },
        error: function (error) {
            console.log(error);
        }
    });
}

function run_exp(alg, container){

    var sampling = $("#sampling-val").val()
    var method = $("#method-val").val()
    var k = $("#k-val-" + container).val()

    if(!validation_hyper()){
        return
    }

    if (k == undefined){
        k = 20;
    }

    if (sampling == "SUSIE") {
        var jump_prob = $("#jump_prob").val()
        var sampl_size = $("#sampl_size").val()
        var min_comp = $("#min_comp").val()
        
        conf = "&p=" + jump_prob + "&s=" + sampl_size + "&t=" + min_comp;
        $.when(run_sampling(jump_prob, sampl_size, min_comp),
                get_evaluation(alg, container, method, conf, k)
        ).done(function(){
            console.log("done!")
        });

    }
    else if (sampling == "no_sampling" || sampling == "No Sampling") {
        conf = "original"
        get_evaluation(alg, container, method, conf, k);
    }

    
}


function run_clusters(alg, container){

    var sampling = $("#sampling-val").val()
    var method = $("#method-val").val()

    if(!validation_hyper()){
        return
    }

    if (sampling == "SUSIE") {
        var jump_prob = $("#jump_prob").val()
        var sampl_size = $("#sampl_size").val()
        var min_comp = $("#min_comp").val()
        
        conf = "&p=" + jump_prob + "&s=" + sampl_size + "&t=" + min_comp;
        $.when(run_sampling(jump_prob, sampl_size, min_comp),
        get_clusters(alg, container, method, conf)
        ).done(function(){
            console.log("done!")
        });

    }
    else if (sampling == "no_sampling" || sampling == "No Sampling") {
        conf = "original"
        get_clusters(alg, container, method, conf);
    }   
}

function run_expl(alg, container){

    var sampling = $("#sampling-val").val()
    var method = $("#method-val").val()

    if(!validation_hyper()){
        return
    }

    if (sampling == "SUSIE") {
        var jump_prob = $("#jump_prob").val()
        var sampl_size = $("#sampl_size").val()
        var min_comp = $("#min_comp").val()
        
        conf = "&p=" + jump_prob + "&s=" + sampl_size + "&t=" + min_comp;
        $.when(run_sampling(jump_prob, sampl_size, min_comp),
        get_explanation(alg, container, method, conf)
        ).done(function(){
            console.log("done!")
        });

    }
    else if (sampling == "no_sampling" || sampling == "No Sampling") {
        conf = "original"
        get_explanation(alg, container, method, conf);
    }   
}

function run_predictions(alg, container){

    var sampling = $("#sampling-val").val()
    var method = $("#method-val").val()

    if(!validation_hyper()){
        return
    }

    if (sampling == "SUSIE") {
        var jump_prob = $("#jump_prob").val()
        var sampl_size = $("#sampl_size").val()
        var min_comp = $("#min_comp").val()
        
        conf = "&p=" + jump_prob + "&s=" + sampl_size + "&t=" + min_comp;
        $.when(run_sampling(jump_prob, sampl_size, min_comp),
        get_predictions(alg, container, method, conf)
        ).done(function(){
            console.log("done!")
        });

    }
    else if (sampling == "no_sampling" || sampling == "No Sampling") {
        conf = "original"
        get_predictions(alg, container, method, conf);
    }

    
}

function isValidHttpUrl(string) {
    let url;
    
    try {
      url = new URL(string);
    } catch (_) {
      return false;  
    }
  
    return url.protocol === "http:" || url.protocol === "https:";
}

function getPostfixFromURL(url) {
    const parts = url.split('/');
    const lastPart = parts[parts.length - 1];
    // const postfix = lastPart.split('.')[1]; // Assumes postfix is the second part after the dot
    return lastPart;
  }

/* Prints the clusters in the 'container_id' html element */
function get_clusters(alg, container_id, method, conf) {


    var method = $("#method-val").val()
    var explanation = 0
    var dataset = $('#dataset-val').val()

    if (has_condition() == false)
        return;

    var dataset_type = $('#dataset-val').select2("data")[0].type
    if (non_cached_datasets.includes(dataset)){
        if(dataset_type == "tab" && document.querySelector('input[name="exp-form"]:checked') == null){
            has_cached_data();
            return;
        }
        if(dataset_type == "tab"){
            explanation = parseInt(document.querySelector('input[name="exp-form"]:checked').value);
        }

        document.getElementById('datasets-info-container').innerHTML = "";
    }

    if (conf == "original"){
        url = "/requests/getClusters?alg=" + alg + "&dataset=" + dataset + "&method=" + method + "&explanation=" + explanation;
    }
    else {
        url = "/requests/getClusters?alg=" + alg + "&dataset=" + dataset + "&method=" + method + "&explanation=" + explanation + conf;
    }
    
    $('#' + container_id).html('<div class="loader"></div><p style="text-align:center; margin-top:1%">Please wait as this may take a few minutes...</p>')

    $.ajax({
        type: "GET",
        url: url,
        contentType: "application/json",
        dataType: 'text',
        success: function (response) {
            var obj = JSON.parse(response);

            //If there is no exception 
            if (obj.exception == undefined) {
                var clusters_data = eval(obj.clusters);

                if (alg == "unfair")
                    $('#unfair-container').html('<label for="clusters-table" id="clusters-label">Suggested Matches</label><div id="clusters-table-' + container_id + '"></div>');
                else
                    $('#fairer-container').html('<label for="clusters-table" id="clusters-label">Suggested Matches</label><div id="clusters-table-' + container_id + '"></div>');
                
                // Create the legend element
                var legend_cont = document.createElement("div");
                legend_cont.id = "legend-cont-clust"
                legend_cont.innerHTML = `<div id="legend-clust">
                <span style="text-color: #eaebf5 !important;">Protected</span>
                <div id="true-rectangle"></div>
                <span style="text-color: #fdece8 !important;">Non protected</span>
                <div id="false-rectangle"></div>
                </div>`

                // Append the legend element to the table container
                var tableContainer = document.querySelector("#clusters-table-" + container_id);
                tableContainer.classList.add("table-bordered", "responsive-table");

                tableContainer.parentNode.insertBefore(legend_cont, tableContainer);
                
                $('#clusters-table' + container_id).addClass("table-bordered responsive-table");
                var table3 = new Tabulator("#clusters-table-" + container_id, {
                    data: clusters_data,           //load row data from array
                    layout: "fitColumns",      //fit columns to width of table
                    responsiveLayout: "hide",  //hide columns that dont fit on the table
                    addRowPos: "top",          //when adding a new row, add it to the top of the table
                    pagination: "local",       //paginate the data
                    paginationSize: 10,         //allow 15 rows per page of data
                    autoColumns: true,
                    rowFormatter: function (row) {
                        var data = row.getData();
                        if (data.Prot === "True") {
                            // Apply CSS class to row for true value
                            row.getElement().classList.add("true-row");
                        } 
                        else if (data.Prot === "False") {
                            // Apply CSS class to row for false value
                            row.getElement().classList.add("false-row");
                        }
                    },
                });

                        start_index_3 = 0
                        table3.on("tableBuilt", function() {
                            table3.hideColumn("Prot");
                            var rows = table3.getRows();
                            let index = start_index_3;
                            for (index = start_index_3; index < (start_index_3 + 10); index++) {
                                var cell1 = rows[index].getCell("KG_1 id");
                                var cell2 = rows[index].getCell("KG_2 id");
                                cell1_val = cell1.getValue()
                                cell2_val = cell2.getValue()
                                
                                if(isValidHttpUrl(cell1_val)){
                                    var link1 = document.createElement("a");
                                    link1.href = cell1_val;
                                    link1.textContent = getPostfixFromURL(cell1_val);
                                    link1.target = "_blank";
                                    cell1.getElement().innerHTML = "";
                                    cell1.getElement().appendChild(link1);
                                }

                                if(isValidHttpUrl(cell2_val)){
                                    var link2 = document.createElement("a");
                                    link2.href = cell2_val;
                                    link2.textContent = getPostfixFromURL(cell2_val);
                                    link2.target = "_blank";
                                    cell2.getElement().innerHTML = "";
                                    cell2.getElement().appendChild(link2);
                                }
                            }
                            start_index_3 = index
                        })

                        table3.on("pageLoaded", function(pageno){
                            var rows = table3.getRows();
                            let magic_num = 10 * (pageno - 1);
                            for (index = magic_num; index < (magic_num + 10); index++) {

                                if(rows[index]){
                                    var cell1 = rows[index].getCell("KG_1 id");
                                    var cell2 = rows[index].getCell("KG_2 id");
                                    cell1_val = cell1.getValue()
                                    cell2_val = cell2.getValue()
                                    
                                    if(isValidHttpUrl(cell1_val)){
                                        var link1 = document.createElement("a");
                                        link1.href = cell1_val;
                                        link1.textContent = getPostfixFromURL(cell1_val);
                                        link1.target = "_blank";
                                        cell1.getElement().innerHTML = "";
                                        cell1.getElement().appendChild(link1);
                                    }

                                    if(isValidHttpUrl(cell2_val)){
                                        var link2 = document.createElement("a");
                                        link2.href = cell2_val;
                                        link2.textContent = getPostfixFromURL(cell2_val);
                                        link2.target = "_blank";
                                        cell2.getElement().innerHTML = "";
                                        cell2.getElement().appendChild(link2);
                                    }
                                }
                                
                            }
                            start_index_3 = index
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
function get_evaluation(alg, container_id, method, conf, k) {
    var explanation = 1;
    var dataset = $('#dataset-val').val()
    if (has_condition() == false)
        return;

    var dataset_type = $('#dataset-val').select2("data")[0].type

    if (non_cached_datasets.includes(dataset)){
        if(dataset_type == "tab" && document.querySelector('input[name="exp-form"]:checked') == null){
            has_cached_data();
            return;
        }

        if(dataset_type == "tab"){
            explanation = parseInt(document.querySelector('input[name="exp-form"]:checked').value);
        } 
        
        document.getElementById('datasets-info-container').innerHTML = "";
    }
    
    $('#' + container_id).html('<div class="loader"></div><p style="text-align:center; margin-top:1%">Please wait as this may take a few minutes...</p>')

    if(conf == "original"){
        url = "/requests/getEvaluationResults?alg=" + alg + "&dataset=" + dataset + "&method=" + method + "&explanation=" + explanation + "&k=" + k
    }
    else{
        url = "/requests/getEvaluationResults?alg=" + alg + "&dataset=" + dataset + "&method=" + method + "&explanation=" + explanation + conf + "&k=" + k
    }
    
    $.ajax({
        type: "GET",
        url: url,
        contentType: "application/json",
        dataType: 'text',
        success: function (response) {
            const obj = JSON.parse(response);
            //If there is exception 
            if (obj.exception == undefined) {         
                $('#' + container_id).html('<label for="eval-table" id="eval-label-' + container_id + '">Evaluation Results</label><div id="eval-table-' + container_id + '"></div>');
                $('#eval-table-' + container_id).addClass("table-bordered responsive-table");

                if(container_id.replace("-container", "") == "fairer"){
                    temp = "fairER"
                }
                else{
                    temp = container_id.replace("-container", "")
                }

                $('#eval-label-' + container_id).append('<br><label for="k-val-' + container_id + '""><b>Set k = </b></label> <input type="text" class="form-control" id="k-val-' + container_id + '" name="k-val-' + container_id + '" value=\"' + k + '\"> <button type="button" class="btn btn-secondary re-run" id="re-run' + container_id + '" onclick="run_exp(\'' + temp + '\', \'' + container_id + '\')">' + 'Run Again' + '</button>');

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
function get_statistics(conf) {
    var explanation = 1
    
    if (has_condition() == false)
        return;

    $('#datasets-info-container').html('<div class="loader"></div><p style="text-align:center; margin-top:1%">Please wait as this may take a few minutes...</p>')
    var dataset = $('#dataset-val').val();
    var dataset_type = $('#dataset-val').select2("data")[0].type

    if (non_cached_datasets.includes(dataset)){
        if(dataset_type == "tab" && document.querySelector('input[name="exp-form"]:checked') == null){
            has_cached_data();
            return;
        }
        
        if(dataset_type == "tab"){
            explanation = parseInt(document.querySelector('input[name="exp-form"]:checked').value);
        }
        document.getElementById('datasets-info-container').innerHTML = "";
    }

    if(conf == "original"){
        url = "/requests/getStatistics?dataset=" + dataset + "&explanation=" + explanation + "&type=" + dataset_type
    }
    else{
        url = "/requests/getStatistics?dataset=" + dataset + "&explanation=" + explanation + "&type=" + dataset_type + conf
    }

    $.ajax({
        type: "GET",
        url: url,
        contentType: "application/json",
        dataType: 'text',
        success: function (response) {
            const obj = JSON.parse(response);
            //If there is no exception 
            if (obj.exception == undefined) {

                $('#datasets-info-container').html('<div id="top-table"><label for="statistics-table">Statistics for KG1/KG2</label><button class="btn btn-secondary data-info-btn" onclick="show_data_descr()">Info</button></div><div id="statistics-table"></div>');
                $('#statistics-table').addClass("table-bordered responsive-table");
                
                data = '[' + response + ']'
                data = JSON.parse(JSON.parse(JSON.stringify(data)));
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

function upload_dataset(dataset_type) {

    if(dataset_type == "kg"){
        var form_data = new FormData($('#kg-upload-form')[0]);
        if (form_data.get("kg-upload-file")["name"].length == 0) {
            pretty_alert('error', 'Error!', 'You did not select a dataset to upload!')
            return;
        }
    }else if(dataset_type == "tab"){
        var form_data = new FormData($('#dataset-upload-form')[0]);
        if (form_data.get("dataset-upload-file")["name"].length == 0) {
            pretty_alert('error', 'Error!', 'You did not select a dataset to upload!')
            return;
        }
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

                    if(dataset_type == "kg"){
                        var dataset_name = form_data.get("kg-upload-file")["name"].slice(0, -4);
                       
                    }else if(dataset_type == "tab"){
                        var dataset_name = form_data.get("dataset-upload-file")["name"].slice(0, -4);
                    }

                    // var option = document.createElement("option");
                    // option.value = dataset_name;
                    // option.text = dataset_name;
                    // document.getElementById('dataset-val').appendChild(option);

                    // document.getElementById('dataset-val').value = dataset_name;

                    clear_all_containers();
                    non_cached_datasets.push(dataset_name);
                    datasets_without_condition.push(dataset_name);
                    has_cached_data();
                    setTimeout(function () { location.reload(); }, 3000);
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
        $('.error-labels-group').removeClass("vis_not_hidden").addClass("vis_hidden");

        $.ajax({
            type: "GET",
            url: "/requests/getDatasetsNames",
            success: function (response) {
                //If there is no exception 
                if (response.exception == undefined) {
                    datasets_names_list = response.datasets_list
                    non_cached_datasets = response.non_cached_datasets

                    datasets_without_condition = response.datasets_without_condition

                    // [TODO] Testing purpose. DELETE IT !
                    // datasets_names_list.length = 0

                    if (datasets_names_list.length == 0) {
                        $("#select-dataset-label").html("")
                        $("#datasets-container").css("display", "block");
                        $("#datasets-container").css("text-align", "center");
                        htmlRes = '<p style="color:red">No datasets found on system!</p>' +
                            '<b><p>Press the button to download the Datasets from DeepMatcher and OpenEA.</b></p>' +
                            '<button type="button" class="btn btn-success" onclick="download_datasets()">Download</button>';
                        $('#datasets-container').html(htmlRes)

                        // Hide if no datasets
                        $('#sampling-val').addClass("hidden");
                        $('#group_labels').addClass("hidden");
                        $('#select-method-label').addClass("hidden");
                        $('#method-val').addClass("hidden");
                        $('.hypers').addClass("hidden");
                    }
                    else {

                        $('#sampling-val').removeClass("hidden");
                        $('#group_labels').removeClass("hidden");
                        $('#select-method-label').removeClass("hidden");
                        $('#method-val').removeClass("hidden");
                        $('.hypers').removeClass("hidden");

                        
                        $('#jump-error').removeClass("vis_not_hidden").addClass("vis_hidden")
                        $('#sampl-error').removeClass("vis_not_hidden").addClass("vis_hidden")
                        $('#min-error').removeClass("vis_not_hidden").addClass("vis_hidden")

                        var data = [];
                        var kg_data = []
                        var tab_data = []
                        datasets_names_list.forEach(item => {
                            if (item.includes("D_W") || item.includes("D_Y")) {
                                if(!item.includes("_RREA") && !item.includes("_BERT_INT")){
                                    type = "kg";
                                    kg_data.push({ id: item, text: item, type: type})
                                }
                            }
                            else if (!item.includes("mdb") && !item.includes("sampled")) {
                                    type = "tab";
                                    tab_data.push({ id: item, text: item, type: type});
                            }
                            data.push({ id: item, text: item, type: type})
                    });
                        $('#datasets-container').html('<select id="dataset-val" style="width:80%;" onchange="has_cached_data()"></select>')
    
                        let statistics_btn = document.createElement("button");
                        statistics_btn.innerHTML = "Dataset Statistics";
                        statistics_btn.className = "btn btn-secondary";
                        statistics_btn.addEventListener("click", function () {
                            
                            var sampling = $("#sampling-val").val()
                            if (sampling == "SUSIE") {
                                var jump_prob = $("#jump_prob").val()
                                var sampl_size = $("#sampl_size").val()
                                var min_comp = $("#min_comp").val()      
                                conf = "&p=" + jump_prob + "&s=" + sampl_size + "&t=" + min_comp;
                                $.when(run_sampling(jump_prob, sampl_size, min_comp),
                                get_statistics(conf)
                                ).done(function(){
                                    console.log("done!")
                                });
                            }
                            else if (sampling == "no_sampling" || sampling == "No Sampling") {
                                conf = "original"
                                get_statistics(conf);
                            }

                        });
                        $("#datasets-container").append(statistics_btn)

                        let upload_btn = document.createElement("button");
                        upload_btn.innerHTML = "Upload Dataset";
                        upload_btn.className = "btn btn-secondary";
                        upload_btn.addEventListener("click", function () {
                            clear_all_containers();
                            upload_dataset_info();
                            upload_kg_info();
                        });
                        $("#datasets-container").append(upload_btn)

                        let delete_btn = document.createElement("button");
                        delete_btn.innerHTML = "Delete Dataset";
                        delete_btn.className = "btn btn-danger";
                        delete_btn.addEventListener("click", function () {
                            delete_dataset_message();
                        });
                        $("#datasets-container").append(delete_btn)

                        $("#datasets-container").append(upload_btn)
    
                        $("#dataset-val").select2({
                            data: [{
                                id: '',
                                text: 'Knowledge Graph',
                                children: kg_data
                            }, {
                            id: '',
                            text: 'Tabular',
                            children: tab_data
                        }]
                        })

                        $('#method-val').select2({
                            data:  [{
                                id: '',
                                text: 'Knowledge Graph',
                                children: [
                                    { id: 'RREA', text: 'RREA' },
                                    { id: 'RDGCN', text: 'RDGCN' },
                                    { id: 'MultiKE', text: 'MultiKE' },
                                    { id: 'BERT_INT', text: 'BERT-INT (requires GPU)' },
                                    { id: 'PARIS', text: 'PARIS' },
                                ]
                            },{
                                id: '',
                                text: 'Tabular',
                                children: [
                                    { id: 'deepmatcher', text: 'Deepmatcher' },
                                ]
                            }]
                        })

                        $("#sampling-val").select2({
                            data: [{
                                id: 'SUSIE',
                                text: 'SUSIE'
                            }, {
                                id: 'no_sampling',
                                text: 'No Sampling'
                            }]
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


/* Downloads Deepmatcher and Knowledge Graph datasets */
function download_datasets() {
    htmlRes = '<b><p>Datasets are dowloading.</b></p><p>Estimated time: 30sec.</p>' +
        '<div class="loader"></div>';
    $('#datasets-container').html(htmlRes)
    $.ajax({
        url: '/requests/downloadDMdatasets',
        type: 'POST',
        success: function (response) {
            //If there is no exception 
            if (response.exception == undefined) {
                // $('#datasets-container').html('')
                Swal.fire({
                    position: 'center',
                    icon: 'success',
                    title: 'Done!',
                    text: 'Datasets for matching tabular data were downloaded.',
                    showConfirmButton: true,
                    // timer: 3000
                }).then((response) => {
                    $.ajax({
                        url: '/requests/downloadKGdatasets',
                        type: 'POST',
                        success: function (response) {
                            //If there is no exception 
                            if (response.exception == undefined) {
                                $('#datasets-container').html('')
                                Swal.fire({
                                    position: 'center',
                                    icon: 'success',
                                    title: 'Done!',
                                    text: 'Datasets for matching knowledge graphs were downloaded.',
                                    showConfirmButton: true,
                                    // timer: 3000
                                }).then((response)=>{

                                    Swal.fire({
                                        position: 'center',
                                        // icon: 'success',
                                        // title: 'The page will be reloaded',
                                        text: 'The page will be reloaded.',
                                        showConfirmButton: false,
                                        timer: 2000
                                    })

                                    setTimeout(function () { location.reload(); }, 3000);
                                  })
                            }
                            //If there is an exception, print details about it
                            else print_exception(response.exception_type, response.exception, response.filename, response.func_name, response.line_number)
                        },
                        error: function (error) {
                            console.log(error);
                        }
                    });
                  });
                // setTimeout(function () { location.reload(); }, 3000);
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
function get_explanation(alg, container_id, method, conf) {

    $('#fairer-container').html('<div class="loader"></div><p style="text-align:center; margin-top:1%">Please wait as this may take a few minutes...</p>')
    
    var dataset = $('#dataset-val').val()
    var method = $("#method-val").val()
    var explanation = 1;

    if (non_cached_datasets.includes(dataset))
        document.getElementById('datasets-info-container').innerHTML = "";

    if (conf == "original"){
        url = "/requests/getExplanation?alg=" + alg + "&dataset=" + dataset + "&method=" + method + "&explanation=" + explanation;
    }
    else {
        url = "/requests/getExplanation?alg=" + alg + "&dataset=" + dataset + "&method=" + method + "&explanation=" + explanation + conf;
    }

    $.ajax({
        type: "GET",
        url: url,
        dataType: 'text',
        success: function (response) {
            const obj = JSON.parse(response);
            //If there is no exception 
            if (obj.exception == undefined) {
                if(method == "deepmatcher"){
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
                    
                    }else{

                        var cands = eval(obj.candidates);
                        var clusters_data1 = []
                        var clusters_data2 = []
                        cands.forEach(function(cand){
                            if(cand["Prot"] == "True"){
                                clusters_data1.push(cand)
                            }else{
                                clusters_data2.push(cand)
                            }
                        });

                        // var clusters_data2 = eval(obj.candidates);
                        var clusters_data3 = eval(obj.clusters);

                        // Create a container div to hold both tables
                        var container = document.createElement("div");
                        container.id = "tables-container";
                        $('#fairer-container').html(container);

                        // Create the first table and append it to the container
                        var tableContainer1 = document.createElement("div");
                        tableContainer1.id = "explanations-table-" + container_id + "-1";
                        tableContainer1.classList.add("table-container");
                        container.appendChild(tableContainer1);

                        // Create the second table and append it to the container
                        var tableContainer2 = document.createElement("div");
                        tableContainer2.id = "explanations-table-" + container_id + "-2";
                        tableContainer2.classList.add("table-container");
                        container.appendChild(tableContainer2);

                        // Create the second table and append it to the container
                        var tableContainer3 = document.createElement("div");
                        tableContainer3.id = "explanations-table-" + container_id + "-3";
                        tableContainer3.classList.add("table-container");
                        container.appendChild(tableContainer3);

                        // Create the legend element for the first table
                        var legend_cont1 = document.createElement("div");
                        legend_cont1.id = "legend-cont"
                        legend_cont1.innerHTML = `
                        <div id="expl-labels">
                            <label for="clusters-table" id="clusters-label">Protected Candidates</label>
                            <label for="clusters-table" id="clusters-label" style="margin-left: 77px;">Non Protected Candidates</label>
                            <label for="clusters-table" id="clusters-label"  style="margin-left: 42px;">Suggested Matches</label>
                        </div>
                        <div id="legend">
                            <span style="text-color: #eaebf5 !important;">Protected</span>
                            <div id="true-rectangle"></div>
                            <span style="text-color: #fdece8 !important;">Non protected</span>
                            <div id="false-rectangle"></div>
                        </div>`

                        // // Append the legend element to the first table container
                        container.parentNode.insertBefore(legend_cont1, container);

                        // Add CSS classes to the table containers for styling
                        tableContainer1.classList.add("table-bordered", "responsive-table");
                        tableContainer2.classList.add("table-bordered", "responsive-table");
                        tableContainer3.classList.add("table-bordered", "responsive-table");
                        tableContainer1.style.marginRight = "10px";
                        tableContainer2.style.marginRight = "10px";


                        var table3 = new Tabulator("#explanations-table-" + container_id + "-3", {
                            data: clusters_data3,
                            layout: "fitColumns",
                            responsiveLayout: "hide",
                            addRowPos: "top",
                            pagination: "local",
                            paginationSize: 10,
                            autoColumns: true,
                            rowFormatter: function (row) {
                                var data = row.getData();
                                if (data.Prot === "True") {
                                    row.getElement().classList.add("true-row");
                                } else if (data.Prot === "False") {
                                    row.getElement().classList.add("false-row");
                                }
                            },
                        });
                        
                        // Initialize the first table
                        var table1 = new Tabulator("#explanations-table-" + container_id + "-1", {
                            data: clusters_data1,
                            height:"100%",
                            layout: "fitColumns",
                            responsiveLayout: "hide",
                            addRowPos: "top",
                            pagination: "local",
                            paginationSize: 10,
                            autoColumns: true,
                            rowFormatter: function (row) {
                                var data = row.getData();
                                if (data.Prot === "True") {
                                    row.getElement().classList.add("true-row");
                                } else if (data.Prot === "False") {
                                    row.getElement().classList.add("false-row");
                                }
                            },
                        });

                        var table2 = new Tabulator("#explanations-table-" + container_id + "-2", {
                            data: clusters_data2,
                            layout: "fitColumns",
                            responsiveLayout: "hide",
                            addRowPos: "top",
                            pagination: "local",
                            paginationSize: 10,
                            autoColumns: true,
                            rowFormatter: function (row) {
                                var data = row.getData();
                                if (data.Prot === "True") {
                                    row.getElement().classList.add("true-row");
                                } else if (data.Prot === "False") {
                                    row.getElement().classList.add("false-row");
                                }
                            },
                        });

                        start_index_3 = 0
                        table3.on("tableBuilt", function() {
                            table3.hideColumn("Prot");
                            var rows = table3.getRows();
                            let index = start_index_3;
                            for (index = start_index_3; index < (start_index_3 + 10); index++) {
                                var cell1 = rows[index].getCell("KG_1 id");
                                var cell2 = rows[index].getCell("KG_2 id");
                                cell1_val = cell1.getValue()
                                cell2_val = cell2.getValue()
                                
                                if(isValidHttpUrl(cell1_val)){
                                    var link1 = document.createElement("a");
                                    link1.href = cell1_val;
                                    link1.textContent = getPostfixFromURL(cell1_val);
                                    link1.target = "_blank";
                                    cell1.getElement().innerHTML = "";
                                    cell1.getElement().appendChild(link1);
                                }

                                if(isValidHttpUrl(cell2_val)){
                                    var link2 = document.createElement("a");
                                    link2.href = cell2_val;
                                    link2.textContent = getPostfixFromURL(cell2_val);
                                    link2.target = "_blank";
                                    cell2.getElement().innerHTML = "";
                                    cell2.getElement().appendChild(link2);
                                }
                            }
                            start_index_3 = index
                        })

                        table3.on("pageLoaded", function(pageno){
                            var rows = table3.getRows();
                            let magic_num = 10 * (pageno - 1);
                            for (index = magic_num; index < (magic_num + 10); index++) {

                                if(rows[index]){
                                    var cell1 = rows[index].getCell("KG_1 id");
                                    var cell2 = rows[index].getCell("KG_2 id");
                                    cell1_val = cell1.getValue()
                                    cell2_val = cell2.getValue()
                                    
                                    if(isValidHttpUrl(cell1_val)){
                                        var link1 = document.createElement("a");
                                        link1.href = cell1_val;
                                        link1.textContent = getPostfixFromURL(cell1_val);
                                        link1.target = "_blank";
                                        cell1.getElement().innerHTML = "";
                                        cell1.getElement().appendChild(link1);
                                    }

                                    if(isValidHttpUrl(cell2_val)){
                                        var link2 = document.createElement("a");
                                        link2.href = cell2_val;
                                        link2.textContent = getPostfixFromURL(cell2_val);
                                        link2.target = "_blank";
                                        cell2.getElement().innerHTML = "";
                                        cell2.getElement().appendChild(link2);
                                    }
                                }
                                
                            }
                            start_index_3 = index
                        });

                        start_index_1 = 0
                        table1.on("tableBuilt", function() {
                            table1.hideColumn("Prot");
                            table1.hideColumn("Rank");
                            table1.hideColumn("Matching Score");
                            var rows = table1.getRows();
                            let index = start_index_1;
                            for (index = start_index_1; index < (start_index_1 + 7); index++) {
                                var isExist = rows[index].getCell("ExistInClust").getValue()
                                var cell1 = rows[index].getCell("KG_1 id");
                                var cell2 = rows[index].getCell("KG_2 id");
                                if(isExist == "False"){
                                    cell1.getElement().classList.add("strikethrough");
                                    cell2.getElement().classList.add("strikethrough");
                                }
                                cell1_val = cell1.getValue()
                                cell2_val = cell2.getValue()
                                
                                if(isValidHttpUrl(cell1_val)){
                                    var link1 = document.createElement("a");
                                    link1.href = cell1_val;
                                    link1.textContent = getPostfixFromURL(cell1_val);
                                    link1.target = "_blank";
                                    cell1.getElement().innerHTML = "";
                                    cell1.getElement().appendChild(link1);
                                }

                                if(isValidHttpUrl(cell2_val)){
                                    var link2 = document.createElement("a");
                                    link2.href = cell2_val;
                                    link2.textContent = getPostfixFromURL(cell2_val);
                                    link2.target = "_blank";
                                    cell2.getElement().innerHTML = "";
                                    cell2.getElement().appendChild(link2);
                                }
                            }
                            start_index_1 = index
                            table1.hideColumn("ExistInClust");
                        })
                        

                        table1.on("pageLoaded", function(pageno){
                            var rows = table1.getRows();
                            let index = start_index_1;
                            for (index = start_index_1; index < (start_index_1 + 10); index++) {
                                var isExist = rows[index].getCell("ExistInClust").getValue()
                                var cell1 = rows[index].getCell("KG_1 id");
                                var cell2 = rows[index].getCell("KG_2 id");
                                if(isExist == "False"){
                                    cell1.getElement().classList.add("strikethrough");
                                    cell2.getElement().classList.add("strikethrough");
                                }
                                cell1_val = cell1.getValue()
                                cell2_val = cell2.getValue()
                                
                                if(isValidHttpUrl(cell1_val)){
                                    var link1 = document.createElement("a");
                                    link1.href = cell1_val;
                                    link1.textContent = getPostfixFromURL(cell1_val);
                                    link1.target = "_blank";
                                    cell1.getElement().innerHTML = "";
                                    cell1.getElement().appendChild(link1);
                                }

                                if(isValidHttpUrl(cell2_val)){
                                    var link2 = document.createElement("a");
                                    link2.href = cell2_val;
                                    link2.textContent = getPostfixFromURL(cell2_val);
                                    link2.target = "_blank";
                                    cell2.getElement().innerHTML = "";
                                    cell2.getElement().appendChild(link2);
                                }
                            }
                            start_index_1 = index
                        });

                        start_index_2 = 0
                        table2.on("tableBuilt", function() {
                            table2.hideColumn("Prot");
                            table2.hideColumn("Rank");
                            table2.hideColumn("Matching Score");
                            table2.setFilter("Prot", "=", "False");
                            var rows = table2.getRows();
                            let index = start_index_2;
                            for (index = start_index_2; index < (start_index_2 + 10); index++) {
                                var isExist = rows[index].getCell("ExistInClust").getValue()
                                var cell1 = rows[index].getCell("KG_1 id");
                                var cell2 = rows[index].getCell("KG_2 id");
                                if(isExist == "False"){
                                    cell1.getElement().classList.add("strikethrough");
                                    cell2.getElement().classList.add("strikethrough");
                                }
                                cell1_val = cell1.getValue()
                                cell2_val = cell2.getValue()
                                
                                if(isValidHttpUrl(cell1_val)){
                                    var link1 = document.createElement("a");
                                    link1.href = cell1_val;
                                    link1.textContent = getPostfixFromURL(cell1_val);
                                    link1.target = "_blank";
                                    cell1.getElement().innerHTML = "";
                                    cell1.getElement().appendChild(link1);
                                }

                                if(isValidHttpUrl(cell2_val)){
                                    var link2 = document.createElement("a");
                                    link2.href = cell2_val;
                                    link2.textContent = getPostfixFromURL(cell2_val);
                                    link2.target = "_blank";
                                    cell2.getElement().innerHTML = "";
                                    cell2.getElement().appendChild(link2);
                                }
                            }
                            start_index_2 = index
                            table2.hideColumn("ExistInClust");
                        })

                        table2.on("pageLoaded", function(pageno){
                            var rows = table2.getRows();
                            let index = start_index_2;
                            for (index = start_index_2; index < (start_index_2 + 10); index++) {
                                var isExist = rows[index].getCell("ExistInClust").getValue()
                                var cell1 = rows[index].getCell("KG_1 id");
                                var cell2 = rows[index].getCell("KG_2 id");
                                if(isExist == "False"){
                                    cell1.getElement().classList.add("strikethrough");
                                    cell2.getElement().classList.add("strikethrough");
                                }
                                cell1_val = cell1.getValue()
                                cell2_val = cell2.getValue()
                                
                                if(isValidHttpUrl(cell1_val)){
                                    var link1 = document.createElement("a");
                                    link1.href = cell1_val;
                                    link1.textContent = getPostfixFromURL(cell1_val);
                                    link1.target = "_blank";
                                    cell1.getElement().innerHTML = "";
                                    cell1.getElement().appendChild(link1);
                                }

                                if(isValidHttpUrl(cell2_val)){
                                    var link2 = document.createElement("a");
                                    link2.href = cell2_val;
                                    link2.textContent = getPostfixFromURL(cell2_val);
                                    link2.target = "_blank";
                                    cell2.getElement().innerHTML = "";
                                    cell2.getElement().appendChild(link2);
                                }
                            }
                            start_index_2 = index
                        });
     
                    }

                    expl_description("tables-container");
                    
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

function control_sampling(){
    
    var sampling_val = $('#sampling-val').select2("data")[0]
    if(sampling_val != undefined) {
        // Disable sampling and KG methods
        if(sampling_val.text == "No Sampling") {
            $('#jump_prob').removeClass("vis_not_hidden").addClass("vis_hidden");
            $('#sampl_size').removeClass("vis_not_hidden").addClass("vis_hidden");
            $('#min_comp').removeClass("vis_not_hidden").addClass("vis_hidden");
            $('.hyp-labels').removeClass("vis_not_hidden").addClass("vis_hidden");
            $('.error-labels-group').removeClass("vis_not_hidden").addClass("vis_hidden");
        }
        else if(sampling_val.text == "SUSIE") {
            $('#jump_prob').removeClass("vis_hidden").addClass("vis_not_hidden");
            $('#sampl_size').removeClass("vis_hidden").addClass("vis_not_hidden");
            $('#min_comp').removeClass("vis_hidden").addClass("vis_not_hidden");
            $('.hyp-labels').removeClass("vis_hidden").addClass("vis_not_hidden");
            $('.error-labels-group').removeClass("vis_hidden").addClass("vis_not_hidden");
        }
    }
}

function validation_hyper() {
    var jump_prob = $('#jump_prob').val()
    var sampl_size = $('#sampl_size').val()
    var min_comp = $('#min_comp').val()

    if(jump_prob < 0 || jump_prob > 1){
        $('#jump-error').removeClass("vis_hidden").addClass("vis_not_hidden")
        return false
    }else{
        $('#jump-error').removeClass("vis_not_hidden").addClass("vis_hidden")
    }

    if(sampl_size <= 0){
        $('#sampl-error').removeClass("vis_hidden").addClass("vis_not_hidden")
        return false
    }else{
        $('#sampl-error').removeClass("vis_not_hidden").addClass("vis_hidden")

    }

    if(min_comp < 1){
        $('#min-error').removeClass("vis_hidden").addClass("vis_not_hidden")
        return false
    }else{
        $('#min-error').removeClass("vis_not_hidden").addClass("vis_hidden")
    }

    return true
}