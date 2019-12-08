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
            $("#alert-container").show();
            $("#alert-container").addClass("alert alert-success");
            $("#alert-container").text("Your LunchNinja services have been " + statusMessage)
            setTimeout(function() { $("#alert-container").fadeOut(); }, 2000);
        },
        error: function () {
            $("#overlay").hide();
            $("#alert-container").show();
            $("#alert-container").addClass("alert alert-danger");
            $("#alert-container").text("Error occured!!");
            setTimeout(function() { $("#alert-container").fadeOut(); }, 2000);
        } 
    })
});