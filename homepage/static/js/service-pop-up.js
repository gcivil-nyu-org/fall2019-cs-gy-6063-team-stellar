var multipleCancelButton = new Choices('#cuisineSelect', {
    //https://bbbootstrap.com/snippets/multiselect-dropdown-list-83601849
    removeItemButton: true,
    maxItemCount:10,
    // searchResultLimit: 5,
    // renderChoiceLimit: 20
});

var multipleCancelButton = new Choices('#interestSelect', {
    //https://bbbootstrap.com/snippets/multiselect-dropdown-list-83601849
    removeItemButton: true,
    maxItemCount: 10,
    // searchResultLimit: 5,
    // renderChoiceLimit: 20
});

var multipleCancelButton = new Choices('#daysSelect', {
    //https://bbbootstrap.com/snippets/multiselect-dropdown-list-83601849
    removeItemButton: true,
    // searchResultLimit: 5,
    // renderChoiceLimit: 20
});

let service_request = {
    "cuisines_priority":"10",
    "department_priority":"10",
    "interests_priority":"10"
}

var rangeSlider = function () {
    var departmentSlider = $('#department_slider'),
        departmentRange = $('#department_slider_range'),
        departmentValue = $('#department_slider_value');

    departmentSlider.each(function () {

        departmentValue.each(function () {
            var departmentValue = $(this).prev().attr('value');
            $(this).html(departmentValue);
        });

        departmentRange.on('input', function () {
            service_request["department_priority"] = this.value;
            debugger;
            $(this).next(departmentValue).html(this.value);
        });
    });

    var cuisineSlider = $('#cuisine_slider'),
        cuisineRange = $('#cuisine_slider_range'),
        cuisineValue = $('#cuisine_slider_value');

    cuisineSlider.each(function () {
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

rangeSlider();


$("div[id^='myModal']").each(function () {
    var currentModal = $(this);
    let formData = {
        department: '',
        school: '',
        cuisines: []
    };

    function showNextModal(){
        currentModal.modal('hide');
        currentModal.closest("div[id^='myModal']").nextAll("div[id^='myModal']").first().modal('show');
    }

    //click next
    currentModal.find('.btn-next').click(function () {
        if (currentModal[0].id == "myModal3"){
            if(! $("#cuisineSelect").val().length){
                alert("Please select atleast 1 cuisine");
            }else{
                showNextModal();
            }
        } else if (currentModal[0].id == "myModal4"){
            if (!$("#interestSelect").val().length) {
                alert("Please select atleast 1 conversation interest");
            } else {
                showNextModal();
            }
        }else{
            showNextModal();
        }
        
    });

    //click prev
    currentModal.find('.btn-prev').click(function () {
        currentModal.modal('hide');
        currentModal.closest("div[id^='myModal']").prevAll("div[id^='myModal']").first().modal('show');
    });
});


//Service request model data
$(document).on('submit', '#service_select_form', function (e) {
    e.preventDefault();
    service_request['service_type'] = $("#serviceSelect option:selected").val();
    service_request['days'] = $("#daysSelect").val();
})

$(document).ready(function () {
    $('#daysSelectContainer').hide();
});


$('#serviceSelect').on('change', function () {
    if (this.value === 'Daily') {
        $('#daysSelectContainer').hide();
    }else{
        $('#daysSelectContainer').show();
    }
})

//School and department request model data
$(document).on('submit', '#school_select_form', function (e) {
    e.preventDefault();
    service_request['school'] = $("#schoolSelect option:selected").val();
    service_request['department'] = $("#departmentSelect option:selected").val();
})

//Department select
$("#departmentSelect").change(function () {
    var department_id = $(this).val();
    $.ajax({
        url: 'ajax/load_school_homepage/',
        data: {
            'department_id': department_id
        },
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            var content = '';
            $.each(data, function (i, item) {
                content += '<option value=' + '\"' + item + '\"' + '>' + item + '</option>'
            });
            $('#schoolSelect').html(content)
        },
    });
});

//School Select
$("#schoolSelect").change(function () {
    var school_id = $(this).val();
    $.ajax({
        url: 'ajax/load_departments_homepage/',
        data: {
            'school_id': school_id
        },
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            var content = '';
            $.each(data, function (i, item) {
                content += '<option value=' + '\"' + item + '\"' + '>' + item + '</option>'
            });
            $('#departmentSelect').html(content)
        },
    });
});

//Cuisine model data
$(document).on('submit', '#cuisine_select_form', function (e) {
    e.preventDefault();
    service_request['cuisine'] = $("#cuisineSelect").val();
})

//Interest model data
$(document).on('submit', '#interest_select_form', function (e) {
    e.preventDefault();
    service_request['interests'] = $("#interestSelect").val();
})

//Priority model data
$(document).on('submit', '#priority_select_form', function (e) {
    e.preventDefault();
    service_request['csrfmiddlewaretoken'] = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    $.ajax({
        type: 'POST',
        url: '/serviceRequest/',
        data: service_request,
        success: function () {
            window.location.href = "/settings/";
            alert("Thank you for using Lunch Ninja! We'll send you a follow-up email when your matching is ready.");
        }
    })
})
