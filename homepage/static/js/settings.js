$(document).ready(function(){
    console.log("hahahahah")
});

$('#serviceToggle').prop('checked', userServiceStatus);

$.urlParam = function(name){
var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results==null){
      return null;
    }
    else{
       return results[1] || 0;
    }
}

if($.urlParam('from') == "service_page_on"){
    $("#alert-container").show();
    $("#alert-container").addClass("alert alert-success");
    $("#alert-container").text("Thank you for using Lunch Ninja! Your Lunch Ninja service has been switched on. We'll send you a follow-up email when your matching is ready.");
    setTimeout(function() { $("#alert-container").fadeOut(); }, 4000);
}else if($.urlParam('from') == "service_page_off"){
    $("#alert-container").show();
    $("#alert-container").addClass("alert alert-success");
    $("#alert-container").text("Thank you for using Lunch Ninja! We'll send you a follow-up email to inform you about your match based on your new preferences!");
    setTimeout(function() { $("#alert-container").fadeOut(); }, 4000);
}

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
            $("#alert-container").text("Your LunchNinja services have been " + statusMessage);
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