/* global $ */

function updateTrainingVisibility(value) {
    if (value === "custom") {$("#training-input").show();}
    else                    {$("#training-input").hide();}
}

$(document).on("change", ":file", function() {
    var input = $(this);
    var label = input.val().replace(/\\/g,"/").replace(/.*\//, "");
    $(this).parent().next("input[type=text]").val(label);
});

$(function() {
    updateTrainingVisibility($("#trainingset").val());

    $("#trainingset").on("change", function() {
        // When you change the selection, we check to see if you need to hide
        // the file input
        updateTrainingVisibility($(this).val());
    });
});