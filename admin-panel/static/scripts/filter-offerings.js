function handleFilterResponse(response) {
    //  set search bar to be blank
    $("#search-bar").val("");
    $("#offerings-table").html(response);
}

// sends a request to the server with the search query and sort method
function filterOfferings() {
    // get variables from inputs
    let searchQuery = $("select").val();
    console.log(searchQuery)
    // encode variables for request
    searchQuery = encodeURIComponent(searchQuery);
    // send request to server
    let url = "./filter_offerings?filter=" + searchQuery
    request = $.ajax({
        type: "GET",
        url: url,
        success: handleFilterResponse
    });
  }