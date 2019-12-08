$(document).ready(function(){
    console.log("hahahahah")
});

$('#serviceToggle').prop('checked', userServiceStatus);

$('#serviceToggle').change(function () {
    $("#overlay").show();
    let toggleState = $(this).prop('checked');
    let statusMessage = toggleState? "activated":"deactivated";
    let update_request = {}
    update_request['csrfmiddlewaretoken'] = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    update_request['service_status'] = toggleState;
    $.ajax({
        type: 'POST',
        url: '/toggle-service/',
        data: update_request,
        success: function () {
            $("#overlay").hide();
            alert("Your LunchNinja services have been " + statusMessage);
        },
        error: function () {
            $("#overlay").hide();
            alert('Unknown error ');
        } 
    })
});