
$(document).ready(function () {
    $('select[multiple]').multiselect();
});

$('#cuisineSelect').multiselect({
    columns: 1,
    placeholder: 'Select Cuisines'
});

$("div[id^='myModal']").each(function () {
    var currentModal = $(this);
    let formData = {
        department: '',
        school: '',
        cuisines: []
    };

    //click next
    currentModal.find('.btn-next').click(function () {
        currentModal.modal('hide');
        currentModal.closest("div[id^='myModal']").nextAll("div[id^='myModal']").first().modal('show');
    });

    //click prev
    currentModal.find('.btn-prev').click(function () {
        currentModal.modal('hide');
        currentModal.closest("div[id^='myModal']").prevAll("div[id^='myModal']").first().modal('show');
    });
});

let service_request = {}

//Service request model data
$(document).on('submit', '#service_select_form', function (e) {
    e.preventDefault();
    service_request['service_type'] = $("#serviceSelect option:selected").val();
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
