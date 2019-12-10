var customTemplates = new Choices('#cuisineSelect', {
    removeItemButton: true,
    maxItemCount: 10,
    callbackOnCreateTemplates: function (strToEl) {
        var classNames = this.config.classNames;
        var itemSelectText = this.config.itemSelectText;
        return {
            choice: function (classNames, data) {
                return strToEl('\
                <div\
                  class="' + String(classNames.item) + ' ' + String(classNames.itemChoice) + ' ' + String(data.disabled ? classNames.itemDisabled : classNames.itemSelectable) + '"\
                  data-select-text="' + String(itemSelectText) + '"\
                  data-choice \
                  ' + String(data.disabled ? 'data-choice-disabled aria-disabled="true"' : 'data-choice-selectable') + '\
                  data-id="' + String(data.id) + '"\
                  data-value="' + String(data.value) + '"\
                  ' + String(data.groupId > 0 ? 'role="treeitem"' : 'role="option"') + '\
                  >\
                  <span style="margin-right:10px;">'+ String(data.label) + String(top_cuisines.includes(parseInt(data.value)) ? '<i class="fa fa fa-line-chart fire-icon"></i></span>' : '<div></div>') + '\
                </div>\
              ');
            },
        };
    },
});

var customTemplates = new Choices('#interestSelect', {
    removeItemButton: true,
    maxItemCount: 10,
    callbackOnCreateTemplates: function (strToEl) {
        var classNames = this.config.classNames;
        var itemSelectText = this.config.itemSelectText;
        return {
            choice: function (classNames, data) {
                return strToEl('\
                <div\
                  class="' + String(classNames.item) + ' ' + String(classNames.itemChoice) + ' ' + String(data.disabled ? classNames.itemDisabled : classNames.itemSelectable) + '"\
                  data-select-text="' + String(itemSelectText) + '"\
                  data-choice \
                  ' + String(data.disabled ? 'data-choice-disabled aria-disabled="true"' : 'data-choice-selectable') + '\
                  data-id="' + String(data.id) + '"\
                  data-value="' + String(data.value) + '"\
                  ' + String(data.groupId > 0 ? 'role="treeitem"' : 'role="option"') + '\
                  >\
                  <span style="margin-right:10px;">'+ String(data.label) + String(top_interests.includes(parseInt(data.value)) ? '<i class="fa fa fa-line-chart fire-icon"></i></span>' : '<div></div>') + '\
                </div>\
              ');
            },
        };
    },
});

var multipleCancelButton = new Choices('#daysSelect', {
    //https://bbbootstrap.com/snippets/multiselect-dropdown-list-83601849
    removeItemButton: true,
    shouldSort: false,
    shouldSortItems: false,
});

let service_request = {
    "cuisines_priority":"5",
    "department_priority":"5",
    "interests_priority":"5"
};

var rangeSlider = function () {
    var departmentSlider = $('#department_slider'),
        departmentRange = $('#department_slider_range'),
        departmentValue = $('#department_slider_value');

    departmentSlider.each(function () {
        service_request["department_priority"] = document.getElementById("department_slider_range").value;

        departmentValue.each(function () {
            var departmentValue = $(this).prev().attr('value');
            $(this).html(departmentValue);
        });

        departmentRange.on('input', function () {
            service_request["department_priority"] = this.value;
            $(this).next(departmentValue).html(this.value);
        });
    });

    var cuisineSlider = $('#cuisine_slider'),
        cuisineRange = $('#cuisine_slider_range'),
        cuisineValue = $('#cuisine_slider_value');

    cuisineSlider.each(function () {
        service_request["cuisines_priority"] = document.getElementById("cuisine_slider_range").value;
        cuisineValue.each(function () {
            var value = $(this).prev().attr('value');
            $(this).html(value);
        });

        cuisineRange.on('input', function () {
            service_request["cuisines_priority"] = this.value;
            $(this).next(cuisineValue).html(this.value);
        });
    });

    var interestSlider = $('#interest_slider'),
        interestRange = $('#interest_slider_range'),
        interestValue = $('#interest_slider_value');

    interestSlider.each(function () {
        service_request["interests_priority"] = document.getElementById("interest_slider_range").value;

        interestValue.each(function () {
            var value = $(this).prev().attr('value');
            $(this).html(value);
        });

        interestRange.on('input', function () {
            service_request["interests_priority"] = this.value
            $(this).next(interestValue).html(this.value);
        });
    });
};


$(document).ready(function () {
    var servicetype=document.getElementById("serviceSelect");
    if (servicetype.name === "Daily"){
        $('#daysSelectContainer').hide();
    }
    else{
        $('#daysSelectContainer').show();
    }
});


function switch_day() {
    console.log("service changed")
    console.log(document.getElementById("serviceSelect").value)
    var daysSelectContainer=document.getElementById("daysSelectContainer");
    if (document.getElementById("serviceSelect").value === 'Daily') {
        daysSelectContainer.style.display = "none";
    } else {
        daysSelectContainer.style.display = "block";
    }
};

$('#serviceSelect').on('change', function () {
    console.log("service changed")
    if (this.value === 'Daily') {
        $('#daysSelectContainer').hide();
    }else{
        $('#daysSelectContainer').show();
    }
});


//Department select
$("#departmentSelect").change(function () {
    var department_id = $(this).val();
    $("#overlay").show();
    $.ajax({
        url: 'ajax/load_school_homepage/',
        data: {
            'department_id': department_id
        },
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            $("#overlay").hide();
            var content = '';
            $.each(data, function (i, item) {
                content += '<option value=' + '\"' + item + '\"' + '>' + item + '</option>'
            });
            $('#schoolSelect').html(content)
        },
        error: function () {
            $("#overlay").hide();
            alert('Unknown error ');
        }
    });
});

//School Select
$("#schoolSelect").change(function () {
    var school_id = $(this).val();
    console.log(school_id)
    $("#overlay").show();
    $.ajax({
        url: 'ajax/load_departments_homepage/',
        data: {
            'school_id': school_id
        },
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            $("#overlay").hide();
            var content = '';
            $.each(data, function (i, item) {
                content += '<option value=' + '\"' + item + '\"' + '>' + item + '</option>'
            });
            $('#departmentSelect').html(content)
        },
        error: function () {
            $("#overlay").hide();
            alert('Unknown error ');
        }
    });
});


//Priority model data
$(document).on('submit', '#service_select_form', function (e) {
    e.preventDefault();
    $("#overlay").show();
    // service_request["department_priority"] = $('#department_slider_range').value;
    service_request['service_type'] = $("#serviceSelect option:selected").val();
    service_request['days'] = $("#daysSelect").val();
    service_request['school'] = $("#schoolSelect option:selected").val();
    service_request['department'] = $("#departmentSelect option:selected").val();
    service_request['cuisine'] = $("#cuisineSelect").val();
    service_request['interests'] = $("#interestSelect").val();
    service_request['csrfmiddlewaretoken'] = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    $.ajax({
        type: 'POST',
        url: '/service/',
        data: service_request,
        success: function () {
            $("#overlay").hide();
            if(service_status == 0){
                window.location.href = "/settings?from=service_page_on";
            }
            else {
                window.location.href = "/settings?from=service_page_off";
            }
        },
        error: function () {
            $("#overlay").hide();
            alert('Unknown error ');
        }
    })
});

rangeSlider();