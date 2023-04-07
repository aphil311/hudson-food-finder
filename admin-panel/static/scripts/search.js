//----------------------------------------------------------------------
// filters.js
// Author: Aidan Phillips
// This file contains the functions that handle the sorting and
// filtering of the search results. Also can toggle the filter view.
//----------------------------------------------------------------------

// sets html of results-list to the response from the server
function handleResponse(response) {
    $("#results-table").html(response);
  }
  
  // sends a request to the server with the search query and sort method
  function search() {
    // get variables from inputs
    let searchQuery = $("#search-bar").val();
    // encode variables for request
    searchQuery = encodeURIComponent(searchQuery);
    // send request to server
    let url = "./search?search=" + searchQuery
    request = $.ajax({
        type: "GET",
        url: url,
        success: handleResponse
    });
  }
  
  // toggles the filter view
  function toggle() {
    $("#filter-view").toggle();
  }
  
  // sets up the page
  function setup() {
    $("#filter-view").hide();
    search();
    $("#filter-button").on("click", toggle);
    $("#search-bar").on("keypress", function(e) {
        if(e.which == 13) {
            search();
        }
    });
    $("input:radio[name ='sort']").on("change", search);
  }
  
  // runs setup when document is ready
  $(document).ready(setup);