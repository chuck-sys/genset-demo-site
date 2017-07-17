/* global $, firebase, sessionID, usingFirebase */
var config = {
    apiKey: "AIzaSyBjM8SOL5rGiUq9gEF6NvBOMAWDO6Vfoqo",
    authDomain: "genset-demo-website.firebaseapp.com",
    databaseURL: "https://genset-demo-website.firebaseio.com",
    storageBucket: "genset-demo-website.appspot.com",
};
firebase.initializeApp(config);

function updateProgressbar(percent) {
    $(".pbar")
    .css("width", percent + "%")
    .attr("aria-valuenow", percent)
    .text(percent + "%");
}

function deleteSession() {
    $.ajax({
        url: "/api/uploads/" + sessionID,
        type: "DELETE",
    })
    .done(function(resp) {
        window.location.href = "/";
    });
}

$(function() {
    if (usingFirebase) {
        var progressRef = firebase.database().ref("sessions/" + sessionID + "/progress");
        var textRef = firebase.database().ref("sessions/" + sessionID + "/text");
        textRef.on("value", function(snapshot) {
            // Add text to output
            $("#output").append(snapshot.val() + "<br>");
        });
        progressRef.on("value", function(snapshot) {
            // Update progress bar
            updateProgressbar(snapshot.val());

            // If we get to 100, call everything off
            if (snapshot.val() >= 100) {
                progressRef.off("value");
                textRef.off("value");
            }
        });
    }

    $.ajaxSetup({
        cache: false
    });

    $.get("/api/uploads/" + sessionID + "/logs", function(data) {
        // Add original log text to output
        $("#output").html(data);
    });
});