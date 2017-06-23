/* global $ */

function updateTrainingVisibility(value) {
    if (value === "custom") {
        $("#training-input").show();
    } else {
        $("#training-input").hide();
    }
}

$(document).on('change', ':file', function() {
    var input = $(this);
    var label = input.val().replace(/\\/g,'/').replace(/.*\//, '');
    input.trigger('fileselect', [label]);
})

$(function() {
    updateTrainingVisibility($("#trainingset").val());

    $("#trainingset").on("change", function() {
        updateTrainingVisibility($(this).val());
    });

    $(':file').on('fileselect', function(evt, label) {
        $(this).parent().next('input[type=text]').val(label);
    });
});