//----------------------------------------------------------------------
// spinner.js
// Author: Aidan Phillips
// This file contains the functions that handle the sorting and
// filtering of the search results. Also can toggle the filter view.
//----------------------------------------------------------------------

// shows the spinner and hides the upload button
function showSpinner() {
    $("#spinner").show();
}

// sets up the page
function setup() {
    $("#spinner").hide();
    $("#file-upload").on("submit", function() {
        showSpinner();
    });
}

// runs setup when document is ready
$(document).ready(setup);