//----------------------------------------------------------------------
// filters.js
// Author: Aidan Phillips
// This file contains the functions that handle the sorting and
// filtering of the search results. Also can toggle the filter view.
//----------------------------------------------------------------------

// sets html of results-list to the response from the server
function handleResponse(response) {
  $("#results-list").html(response);
}

// sends a request to the server with the search query and sort method
function search() {
  // get variables from inputs
  let searchQuery = $("#search-bar").val();
  let sortBy = $("input:radio[name ='sort']:checked").val();
  if (sortBy === undefined) {
    sortBy = "offerings.title";
  }
  // encode variables for request
  searchQuery = encodeURIComponent(searchQuery);
  sortBy = encodeURIComponent(sortBy);
  // send request to server
  let url = "./search?search=" + searchQuery + "&sort=" + sortBy;

  // deal with services
  let services = [];
  $.each($("input:checkbox[name ='service']:checked"), function() {
    services.push($(this).val());
  });
  if (services.length === 0) {
    $.each($("input:checkbox[name ='service']:not(:checked)"), function() {
      services.push($(this).val());
    });
  }
  for (let i = 0; i < services.length; i++) {
    url += "&service=" + encodeURIComponent(services[i]);
  }

  // deal with times
  startTime = $("#start-time").val();
  if (startTime === "") {
    startTime = "00:00";
  }
  endTime = $("#end-time").val();
  if (endTime === "") {
    endTime = "23:59";
  }
  url += "&start_time=" + encodeURIComponent(startTime);
  url += "&end_time=" + encodeURIComponent(endTime);

  // deal with days
  let days = "";
  $.each($("input:checkbox[name ='day']"), function() {
    if ($(this).is(":checked")) {
      days += "T-";
    } else {
      days += "_-";
    }
  });
  days = days.slice(0, -1);
  url += "&days=" + encodeURIComponent(days);

  // deal with groups
  let groups = [];
  $.each($("input:checkbox[name ='group']:checked"), function() {
    groups.push($(this).val());
  });
  if (groups.length === 0) {
    $.each($("input:checkbox[name ='group']:not(:checked)"), function() {
      groups.push($(this).val());
    });
  }
  for (let i = 0; i < groups.length; i++) {
    url += "&group=" + encodeURIComponent(groups[i]);
  }
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
  $("#search-bar").on("keyup", search);
  $("input:radio[name='sort']").on("change", search);
  $("input:checkbox").on("change", search);
}

// runs setup when document is ready
$(document).ready(setup);