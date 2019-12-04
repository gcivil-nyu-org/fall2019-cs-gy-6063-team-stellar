$(document).ready(function () {
    var $progressDiv = $("#progressBar");
    var $progressBar = $progressDiv.progressStep();
    $progressBar.addStep("Select Preferences");
    $progressBar.addStep("Waiting to get matched");
    $progressBar.addStep("Go out for lunch");

    if (next_lunch_status == 1){
        $progressBar.setCurrentStep(2);
        $progressBar.setAleadyVisited(1);
        $progressBar.setAleadyVisited(0);
    } else if (next_lunch_status == 0 && preference_selected_status == 1){
        $progressBar.setAleadyVisited(0);
        $progressBar.setCurrentStep(1);
    } else if (preference_selected_status == 1){
        $progressBar.setCurrentStep(0);
    }
    $progressBar.refreshLayout();
    $("text").first().attr("x", "50")
    $("text:nth-last-child(2)").last().attr("x", $progressBar.width()-40)
});
