function handleResponse(response) {
  $('#results-list').html(response);
}
function search() {
  let searchQuery = $('#search-bar').val();
  let sortBy = $("input:radio[name ='sort']:checked").val();
  if (sortBy == undefined) {
    sortBy = 'offerings.title';
  }
  searchQuery = encodeURIComponent(searchQuery);
  let url = './search?search=' + searchQuery + '&sort=' + sortBy;
  request = $.ajax({
      url: url,
      type: 'GET',
      success: handleResponse
  });
}

function toggle() {
  $('#filter-view').toggle();
};

function setup() {
  $('#filter-view').hide();
  search();
  $('#filter-button').on('click', toggle);
  $('#search-bar').on('keyup', search);
}

$(document).ready(setup);