function handleResponse(response) {
  $('#results-list').html(response);
}
function search() {
  let searchQuery = $('#search-bar').val();
  searchQuery = encodeURIComponent(searchQuery);
  let sort = 'Offering.title'
  let url = './search?search=' + searchQuery + '&sort=' + sort;
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
  console.log('hi');
  $('#filter-view').hide();
  search();
  $('#filter-button').on('click', toggle);
  $('#search-bar').on('keyup', search);
}

$(document).ready(setup);