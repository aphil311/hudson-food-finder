//----------------------------------------------------------------------
// filters.js
// Author: Aidan Phillips
// This file contains the functions that handle the sorting and
// filtering of the search results. Also can toggle the filter view.
//----------------------------------------------------------------------

// sets html of results-list to the response from the server
function handleResponse(response) {
    $("#current-panel").html(response);
}

// sends a request to the server with the search query and sort method
function searchOfferings() {
  // get variables from inputs
  let searchQuery = $("#search-bar").val();
  // encode variables for request
  searchQuery = encodeURIComponent(searchQuery);
  // send request to server
  let url = "./search_offerings?search=" + searchQuery
  request = $.ajax({
      type: "GET",
      url: url,
      success: handleResponse
  });
}

// sets up the page
function setup() {
  searchOfferings();
  $("#search-bar").on("keypress", function(e) {
      // 13 is *nearly* always the enter key
      if(e.which == 13) {
          search();
      }
  });
  $("#search-btn").on("click", searchOfferings);
}

// runs setup when document is ready
$(document).ready(setup);