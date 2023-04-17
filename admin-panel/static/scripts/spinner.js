//----------------------------------------------------------------------
// spinner.js
// Author: Aidan Phillips
// This file contains the functions that handle the sorting and
// filtering of the search results. Also can toggle the filter view.
//----------------------------------------------------------------------

// sets html of results-list to the response from the server
function submitFile() {
    $("#spinner").show();
    $("form").submit();
}

// sets up the page
function setup() {
    $("#spinner").hide();
    $("#submit-btn").on("click", submitFile);
}

// runs setup when document is ready
$(document).ready(setup);