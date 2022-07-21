function has_condition() {
    var dataset = $('#dataset-val').val();
    if (datasets_without_condition.includes(dataset)) {
        swalWithBootstrapButtons.fire({
            icon: 'info',
            title: 'Oops...',
            text: 'Can\'t perform this operation because there is no protected condition for this dataset yet!',
            footer: 'Open "Protected Tuples" tab, then press "Edit Condition" button and set the condition of your choice.'
        })
        return false
    }
    else
        return true
}

function has_cached_data() {
    var dataset = $('#dataset-val').val();
    clear_all_containers();

    if (non_cached_datasets.includes(dataset)){

        let exp_container = document.createElement('div');
        exp_container.id = 'explanation-check-container';

        let inner_container = document.createElement('div');
        inner_container.className = 'inner-container';

        let form_label = document.createElement('label');
        form_label.innerHTML = 'Do you need explanations?'
        form_label.htmlFor = "exp-form";


        let button = document.createElement('button');
        button.id = 'hide-btn';
        button.className = 'btn btn-light'
        button.innerHTML = 'Hide';
        button.addEventListener("click", function () {
            document.getElementById('datasets-info-container').innerHTML = "";
        });



        let form = document.createElement('form');
        form.id = 'exp-form';


        let input1 = document.createElement('input');
        input1.type = 'radio';
        input1.id = "yes";
        input1.name = "exp-form";
        input1.value = "1";
        input1.checked = "true";

        let yes_label = document.createElement('label');
        yes_label.innerHTML = 'Yes'
        yes_label.htmlFor = "yes";

        let input2 = document.createElement('input');
        input2.type = 'radio';
        input2.id = "no";
        input2.name = "exp-form";
        input2.value = "0";

        let no_label = document.createElement('label');
        no_label.innerHTML = 'No'
        no_label.htmlFor = "no";

        form.appendChild(input1);
        form.appendChild(yes_label);
        form.appendChild(input2);
        form.appendChild(no_label);

        let p = document.createElement('p');
        p.innerHTML = 'It will save you up some time in case you will need them later!'

        inner_container.appendChild(form_label);
        inner_container.appendChild(button);
        inner_container.appendChild(form);
        inner_container.appendChild(p);

        exp_container.appendChild(inner_container);

        document.getElementById('datasets-info-container').append(exp_container);
    }   
}



function delete_dataset_message() {
    var dataset = $('#dataset-val').val();
    Swal.fire({
        title: 'Are you sure?',
        html: "You are going to delete dataset <b>\"" + dataset + "\"</b>. You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!'
    }).then((result) => {
        if (result.isConfirmed) {
            delete_dataset(dataset)
        }
    })
}

function upload_dataset_info() {
    var htmlRes = '<div id="upload-dataset">'
        + '<div id="upload-instructions">'
        + '<p><b>Instructions to upload your dataset</b></p>'
        + '<ol>'
        + '<li>The dataset should be a zip file.</li>'
        + '<li>The zip file name will be the name of the dataset.</li>'
        + '<li>The zip file should contain the following (5) files (no sub-folders!)'
        + '<ul>'
        + '<li>tableA.csv</li>'
        + '<li>tableB.csv</li>'
        + '<li>test.csv</li>'
        + '<li>valid.csv</li>'
        + '<li>train.csv</li>'
        + '</ul>'
        + '</li>'
        + '<li>Your dataset should be structured as '
        + '<a href="https://github.com/anhaidgroup/deepmatcher/blob/master/Datasets.md"'
        + 'target="_blank">Deepmatcher Datasets</a>.</li>'
        + '<li>Once you upload your dataset, it will be available on the dataset selection dropdown.</li>'
        + '</ol>'
        + '</div>'
        + '<div class="mb-3">'
        + '<form enctype="multipart/form-data" id="dataset-upload-form">'
        + '<label for="dataset-upload-file" class="form-label">Upload your dataset</label>'
        + '<input class="form-control" name="dataset-upload-file" type="file" id="dataset-upload-file" accept=".zip">'
        + '<button type="button" class="btn btn-success" onclick="upload_dataset()">Upload</button>'
        + '</form>'
        + '</div>'
        + '</div>'
    $('#datasets-info-container').html(htmlRes)
}

function edit_condition() {
    var htmlRes = '<div class="mb-3">' +
        '<div id="current-protected-condition"></div>' +
        '</div><br>';
    $('#protected-container').html(htmlRes)
    get_condition('current-protected-condition')
    show_condition_input_fields('protected-container')
}

function show_condition_input_fields(container_id) {
    let container = document.createElement('div');
    container.className = 'change-cond-container';

    let left_tuple_container = document.createElement('div');
    left_tuple_container.className = 'left-tuple';

    let left_label = document.createElement('label');
    left_label.innerHTML = '<b>Left Table Attribute</b>'
    left_label.className = "form-label";
    left_label.htmlFor = "left-tpl";

    let left_select = document.createElement('select'); 
    left_select.id = 'left-tpl';
    left_select.className = 'form-select';

    let left_func = document.createElement('select'); 
    left_func.id = 'left-func-select'
    let left_option1 = document.createElement('option');
    left_option1.text = 'contains';
    left_option1.value = 'in'
    left_func.add(left_option1);
    let left_option2 = document.createElement('option');
    left_option2.text = 'starts with';
    left_option2.value = 'startswith'
    left_func.add(left_option2);
    let left_option3 = document.createElement('option');
    left_option3.text = 'is';
    left_option3.value = '=='
    left_func.add(left_option3);

    let left_value = document.createElement('input');
    left_value.type = "text";
    left_value.className = 'form-control';
    left_value.id = 'left-value'

    left_tuple_container.appendChild(left_label);
    left_tuple_container.appendChild(left_select);
    left_tuple_container.appendChild(left_func);
    left_tuple_container.appendChild(left_value);

    
    let logical_op = document.createElement('select'); 
    logical_op.id = 'logical-op-select'
    let log_op_option1 = document.createElement('option');
    log_op_option1.text = 'or';
    log_op_option1.value = 'or'
    logical_op.add(log_op_option1);
    let log_op_option2 = document.createElement('option');
    log_op_option2.text = 'and';
    log_op_option2.value = 'and'
    logical_op.add(log_op_option2);



    let right_tuple_container = document.createElement('div');
    right_tuple_container.className = 'right-tuple';

    let right_label = document.createElement('label');
    right_label.innerHTML = '<b>Right Table Attribute</b>'
    right_label.className = "form-label";
    right_label.htmlFor = "right-tpl";

    let right_select = document.createElement('select'); 
    right_select.id = 'right-tpl';
    right_select.className = 'form-select';

    let right_func = document.createElement('select'); 
    right_func.id = 'right-func-select'
    let right_option1 = document.createElement('option');
    right_option1.text = 'contains';
    right_option1.value = 'in'
    right_func.add(right_option1);
    let right_option2 = document.createElement('option');
    right_option2.text = 'starts with';
    right_option2.value = 'startswith'
    right_func.add(right_option2);
    let right_option3 = document.createElement('option');
    right_option3.text = 'is';
    right_option3.value = '=='
    right_func.add(right_option3);

    let right_value = document.createElement('input');
    right_value.type = "text";
    right_value.className = 'form-control';
    right_value.id = 'right-value'

    right_tuple_container.appendChild(right_label);
    right_tuple_container.appendChild(right_select);
    right_tuple_container.appendChild(right_func);
    right_tuple_container.appendChild(right_value);



    container.appendChild(left_tuple_container);
    container.appendChild(logical_op);
    container.appendChild(right_tuple_container);


    let button_container = document.createElement('div');
    button_container.className = 'button-container';

    let btn = document.createElement("button");
    btn.innerHTML = "Save new condition";
    btn.className = "btn btn-success";
    btn.addEventListener("click", function () {
        post_protected_condition()
    });
    button_container.appendChild(btn)

    document.getElementById(container_id).appendChild(container);
    document.getElementById(container_id).appendChild(button_container);
    fill_dropdowns();
}

function fill_dropdowns() {
    var dataset = $('#dataset-val').val()
    $.ajax({
        type: "GET",
        url: "/requests/getTableAttributes?dataset=" + dataset + "&table=left",
        contentType: "application/json",
        dataType: 'text',
        success: function (response) {
            var obj = JSON.parse(response);
            first_attr = obj.shift();
            $('#left-tpl').html('<option value="' + first_attr + '" selected>' + first_attr + '</option>')

            obj.forEach(item =>
                $('#left-tpl').append('<option value="' + item + '">' + item + '</option>')
            );
        },
        error: function (error) {
            console.log(error);
        }
    });
    $.ajax({
        type: "GET",
        url: "/requests/getTableAttributes?dataset=" + dataset + "&table=right",
        contentType: "application/json",
        dataType: 'text',
        success: function (response) {
            var obj = JSON.parse(response);
            first_attr = obj.shift();
            $('#right-tpl').html('<option value="' + first_attr + '" selected>' + first_attr + '</option>')
            obj.forEach(item =>
                $('#right-tpl').append('<option value="' + item + '">' + item + '</option>')
            );
        },
        error: function (error) {
            console.log(error);
        }
    });
}



/* Radio button (right or left) to choose one of the tables */
function get_table_options() {
    $("#is-protected-result").html('');
    var container = document.getElementById('protected-container');
    container.innerHTML = "";

    let div1 = document.createElement('div');
    div1.className = "form-check";

    let radio_label = document.createElement('label');
    radio_label.innerHTML = "<p><b>Left or Right Tuple:</p></b>"
    container.appendChild(radio_label);
    

    let input1 = document.createElement('input');
    input1.className = "form-check-input";
    input1.type = "radio";
    input1.id = "left-radio";
    input1.addEventListener("click", function () {
        get_attributes('left')
    });

    let label1 = document.createElement('label');
    label1.className = "form-check-label";
    label1.htmlFor = "left-radio";
    label1.innerHTML = "Left";

    div1.appendChild(input1);
    div1.appendChild(label1);


    let div2 = document.createElement('div');
    div2.className = "form-check";

    let input2 = document.createElement('input');
    input2.className = "form-check-input";
    input2.type = "radio";
    input2.id = "right-radio";
    input2.addEventListener("click", function () {
        get_attributes('right')
    });

    let label2 = document.createElement('label');
    label2.className = "form-check-label";
    label2.htmlFor = "right-radio";
    label2.innerHTML = "Right";

    div2.appendChild(input2);
    div2.appendChild(label2);

    container.appendChild(div1);
    container.appendChild(div2);
}

/* Show tuple's attributes as input fields */
function tuple_attributes_to_input(attr_list, table) {
    $('#protected-container').html('')

    var protected_container = document.getElementById('protected-container')
    let container = document.createElement('div');
    container.id = "tuple-container";

    let form = document.createElement('form');
    form.id = "attr-form";
    let label = document.createElement('label');
    label.className = "title";
    label.htmlFor = "attr-form";
    label.innerHTML = "Fill in the fields manually"
    form.appendChild(label);
    let div, input;
    for (var value of attr_list) {
        div = document.createElement('div');

        label = document.createElement('label');
        label.className = "form-label";
        label.htmlFor = value;
        label.innerHTML = "<b>" + value + "</b>";

        input = document.createElement('input');
        input.className = "form-control";
        input.type = "text";
        input.id = value;

        div.appendChild(label);
        div.appendChild(input);
        form.appendChild(div);
    }

    let btn = document.createElement("button");
    btn.innerHTML = "Check";
    btn.className = "btn btn-success";
    btn.addEventListener("click", function () {
        tuple_is_protected(table)
    });
    div = document.createElement('div');
    div.className = "form-container";

    div.appendChild(form)
    div.appendChild(btn)
    container.appendChild(div);

    let p = document.createElement("p");
    p.id = "or-keyword";
    p.innerHTML = "<b>or</b>";

    container.appendChild(p);

    let div2 = document.createElement("div");
    div2.className = "mb-3";

    let json_form = document.createElement("form");
    json_form.enctype = "multipart/form-data";
    json_form.id = "json-upload-form";

    label = document.createElement('label');
    label.className = "form-label";
    label.htmlFor = "json-upload-file";
    label.innerHTML = "Upload your json file";

    input = document.createElement('input');
    input.className = "form-control";
    input.name = "json-upload-file"
    input.type = "file";
    input.id = "json-upload-file";
    input.accept = ".json";

    let upload_btn = document.createElement("button");
    upload_btn.className = "btn btn-success";
    upload_btn.type = "button";
    upload_btn.innerHTML = "Upload";
    upload_btn.addEventListener("click", function () {
        tuple_is_protected_JSON(table)
    });

    let json_info_btn = document.createElement("button");
    json_info_btn.className = "btn btn-link";
    json_info_btn.type = "button";
    json_info_btn.innerHTML = "JSON file structure";
    json_info_btn.addEventListener("click", function () {
        json_tupple_info();
    });

    json_form.appendChild(label);
    json_form.appendChild(input);
    json_form.appendChild(upload_btn);
    json_form.appendChild(json_info_btn);

    div2.appendChild(json_form);
    container.appendChild(div2);

    protected_container.appendChild(container);
}

/* Message showing the right json structure to represent a tuple */
function json_tupple_info() {
    JSONsample = '{ "<b>attributes</b>" : [ <br>'
        + '<span class="tab"></span>   { "Beer_Name" : "Rocket City Red" },<br>'
        + '<span class="tab"></span>   { "Brew_Factory_Name" : "Tarraco Beer"},<br>'
        + '<span class="tab-bg"></span>   ...          <br>'
        + '<span class="tab"></span>   { "AttributeN" : "valueN"}<br>'
        + '] }';

    swalWithBootstrapButtons.fire({
        position: 'center',
        icon: 'info',
        title: 'Example',
        html: JSONsample,
        confirmButtonText: 'Ok',
    })
}
/* Show pair's attributes as input fields */
function pair_attributes_to_input(right_obj, left_obj) {
    var protected_container = document.getElementById("protected-container");
    protected_container.innerHTML = "";

    let container = document.createElement('div');
    container.id = "pair-container";



    var form = document.createElement('form');
    form.id = "attr-form";
    var label = document.createElement('label');
    label.className = "title";
    label.htmlFor = "attr-form";
    label.innerHTML = "Fill in the fields manually"
    form.appendChild(label);

    let h2 = document.createElement('h2');
    h2.innerHTML = "<br>Right Table Attributes<br>"
    form.appendChild(h2);



    for (var value of right_obj) {
        let div = document.createElement('div');
        label = document.createElement('label');
        label.htmlFor = "right-" + value;
        label.className = "form-label";
        label.innerHTML = value;
        div.appendChild(label);


        let input = document.createElement('input');
        input.type = "text";
        input.className = "form-control";
        input.id = "right-" + value;
        div.appendChild(input);

        form.appendChild(div);
    }

    h2 = document.createElement('h2');
    h2.innerHTML = "<br><br><br>Left Table Attributes<br>"
    form.appendChild(h2);



    for (var value of left_obj) {
        let div = document.createElement('div');
        label = document.createElement('label');
        label.htmlFor = "left-" + value;
        label.className = "form-label";
        label.innerHTML = value;
        div.appendChild(label);

        let input = document.createElement('input');
        input.type = "text";
        input.className = "form-control";
        input.id = "left-" + value;
        div.appendChild(input);

        form.appendChild(div);
    }


    let check_btn = document.createElement("button");
    check_btn.className = "btn btn-success";
    check_btn.type = "button";
    check_btn.innerHTML = "Check";
    check_btn.addEventListener("click", function () {
        pair_is_protected()
    });
    form.appendChild(check_btn);

    container.appendChild(form);


    let p = document.createElement("p");
    p.id = "or-keyword";
    p.innerHTML = "<b>or</b>";
    container.appendChild(p);

    let div = document.createElement("div");
    div.className = "mb-3";

    form = document.createElement('form');
    form.enctype = "multipart/form-data";
    form.id = "json-upload-form";

    label = document.createElement("label");
    label.htmlFor = "json-upload-file";
    label.className = "form-label";
    label.innerHTML = "Upload your json file";
    form.appendChild(label);

    let input = document.createElement("input");
    input.name = "json-upload-file";
    input.className = "form-control";
    input.type = "file";
    input.id = "json-upload-file";
    input.accept = ".json";
    form.appendChild(input);

    let upload_btn = document.createElement("button");
    upload_btn.className = "btn btn-success";
    upload_btn.type = "button";
    upload_btn.innerHTML = "Upload";
    upload_btn.addEventListener("click", function () {
        pair_is_protected_JSON()
    });
    form.appendChild(upload_btn);

    let json_info_btn = document.createElement("button");
    json_info_btn.className = "btn btn-link";
    json_info_btn.type = "button";
    json_info_btn.innerHTML = "JSON file structure";
    json_info_btn.addEventListener("click", function () {
        json_pair_info()
    });
    form.appendChild(json_info_btn);
    div.appendChild(form);

    container.appendChild(div);

    protected_container.appendChild(container);
}


/* Message showing the right json structure to represent a pair */
function json_pair_info() {
    JSONsample = '{ "<b>tables</b>" : [<br>'
        + '<span class="tab"></span>   { <b>"left"</b>: [<br>'
        + '<span class="tab-bg"></span>   { "Beer_Name": "Rocket City Red" }, <br>'
        + '<span class="tab-bg"></span>   { "Brew_Factory_Name": "Tarraco Beer" },<br>'
        + '<span class="tab-bg"></span><span class="tab"></span>   ...<br>'
        + '<span class="tab-bg"></span>   { "LAttributeN": "LValueN" } <br>'
        + '<span class="tab"></span>   ] },<br>'
        + '<span class="tab"></span>      { <b>"right"</b>: [<br>'
        + '<span class="tab-bg"></span>   { "Beer_Name": "Rocket City Red" }, <br>'
        + '<span class="tab-bg"></span>   { "Brew_Factory_Name": "Tarraco Beer" },<br>'
        + '<span class="tab-bg"></span><span class="tab"></span>   ...<br>'
        + '<span class="tab-bg"></span>   { "RAttributeM": "RValueM" } <br>'
        + '<span class="tab"></span>   ] }<br>'
        + '] }<br>';

    swalWithBootstrapButtons.fire({
        width: 630,
        position: 'center',
        icon: 'info',
        title: 'Example',
        html: JSONsample,
        confirmButtonText: 'Ok',
    })
}


/* Return 'right' if the param 'str' begins with the word "right"
   otherwise return 'left' */
function attr_prefix(str) {
    var temp = str.substring(0, 5);
    if (temp == 'right')
        return temp;
    else
        return 'left';
}

/* Removes the prefix ("right" or "left") from the 'str' */
function clear_prefix(str) {
    if (attr_prefix(str) == 'right')
        return str.substring(6);
    else
        return str.substring(5);
}



/* Description of evaluation results */
function eval_res_description(container_id){
    accuracy = 'Accuracy@𝑘: out of 𝑘 returned matches, '
        +'how many are correct (i.e., in the ground truth of known matches)? Bias@𝑘: following '
        +'the fairness constraint 𝐹 defined earlier as | (|𝑅𝑝|/𝑘) − (|𝑅𝑛 |/𝑘) | = 𝜖∗, we report '
        +'the values of (|𝑅𝑝|/𝑘) − (|𝑅𝑛 |/𝑘), with negative values denoting favoring the non-protected '
        +'group, zero implying no bias, and positive values favoring the protected group.';

    spd = 'The statistical parity difference is a measure of bias, with SPD = 0 indicating no bias '
        +'(i.e., fair results), while |SPD| = 1 indicates a completely biased algorithm in favor of (SPD = 1), '
        +'or against (SPD = -1) the protected group. In more detail, SPD is defined as follows:<br> '
        +'SPD = Pr(y\'=1|p=1)-Pr(y\'=1|p=0), where y\'=1 indicates that the algorithm suggests a record pair to be '
        +'matching and p=1 (resp. p=0) indicates that this pair is protected (resp. nonprotected).';

    eod = 'The equality of opportunity difference is another measure of bias, with EOD = 0, again, indicating '
        +'no bias (i.e., fair results), and |EOD = 1| indicating a completely biased algorithm. In more detail, '
        +'EOD is defined as follows:<br> EOD = Pr(y\'=1|y=1,p=1)-Pr(y\'=1|y=1,p=0), where y\'=1 indicates that the '
        +'algorithm suggests a record pair to be matching, y=1 indicates that the pair is known to be matching '
        +'(from the ground truth), and p=1 (resp. p=0) indicates that this pair is protected (resp. nonprotected).';


    let container = document.createElement("div"); 
    container.className = "eval-description";
    
    let title = document.createElement("h1");
    title.innerHTML = 'Evaluation Results Description';

    let grid_container = document.createElement("div");
    
    let accuracy_container =  document.createElement("div");
    accuracy_container.className = 'accuracy-container';
    let accuracy_title = document.createElement("h2");
    accuracy_title.innerHTML = 'Accuracy';
    accuracy_container.appendChild(accuracy_title);
    let accuracy_descr = document.createElement("p");
    accuracy_descr.innerHTML = accuracy;
    accuracy_container.appendChild(accuracy_descr);

    let spd_container =  document.createElement("div");
    spd_container.className = 'spd-container';
    let spd_title = document.createElement("h2");
    spd_title.innerHTML = 'SPD';
    spd_container.appendChild(spd_title);
    let spd_descr = document.createElement("p");
    spd_descr.innerHTML = spd;
    spd_container.appendChild(spd_descr);

    let eod_container =  document.createElement("div");
    eod_container.className = 'eod-container';
    let eod_title = document.createElement("h2");
    eod_title.innerHTML = 'EOD';
    eod_container.appendChild(eod_title);
    let eod_descr = document.createElement("p");
    eod_descr.innerHTML = eod;
    eod_container.appendChild(eod_descr);


    container.appendChild(title);
    grid_container.appendChild(accuracy_container);
    grid_container.appendChild(spd_container);
    grid_container.appendChild(eod_container);
    container.appendChild(grid_container);

    document.getElementById(container_id).appendChild(container);
}

function print_exception(type, exception, file, func, line) {
    exception_details = '<b>Exception Type:</b> ' + type.replace(/<|>/g, '') +
        '<br><b>Exception:</b> ' + exception +
        '<br><b>File Name:</b> ' + file +
        '<br><b>Function Name:</b> ' + func +
        '<br><b>Line Number:</b> ' + line
    swalWithBootstrapButtons.fire({
        icon: 'error',
        title: 'Error...',
        html: exception_details
    }).then(() => {
        location.reload();
    })
}

function pretty_alert(icon, title, text) {
    swalWithBootstrapButtons.fire({
        position: 'center',
        icon: icon,
        title: title,
        html: '<p style="text-align: center">' + text + '</p>',
        timer: 3200,
        showConfirmButton: false,
    })
}

function clear_all_containers(){
    document.getElementById('fairer-container').innerHTML = "";
    document.getElementById('unfair-container').innerHTML = "";
    document.getElementById('datasets-info-container').innerHTML = "";
    document.getElementById('protected-container').innerHTML = "";
    document.getElementById('general-container').innerHTML = "";
    document.getElementById('statistics-container').innerHTML = "";
}

function remove_from_noncached_datasets(dataset){
    non_cached_datasets.splice(non_cached_datasets.indexOf(dataset));
}


const swalWithBootstrapButtons = Swal.mixin({
    customClass: {
        confirmButton: 'btn btn-secondary',
    },
    buttonsStyling: false
})

var datasets_without_condition = [];
var non_cached_datasets = [];