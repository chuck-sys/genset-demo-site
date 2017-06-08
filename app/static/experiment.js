/* global $ */

function updateTrainingVisibility(value) {
    if (value === "custom") {
        $("#trainingcsv").show();
    } else {
        $("#trainingcsv").hide();
    }
}

$(function() {
    // Hide as default
    updateTrainingVisibility($("#trainingset").val());
    
    $("#trainingset").on("change", function() {
        updateTrainingVisibility(this.value);
    });
});