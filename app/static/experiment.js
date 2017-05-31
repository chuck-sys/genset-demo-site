/* global $ */

function updateTrainingVisibility(value) {
    if (value === "custom") {
        $("#trainingzip").show();
    } else {
        $("#trainingzip").hide();
    }
}

$(function() {
    // Hide as default
    updateTrainingVisibility($("#trainingset").val());
    
    $("#trainingset").on("change", function() {
        updateTrainingVisibility(this.value);
    });
});