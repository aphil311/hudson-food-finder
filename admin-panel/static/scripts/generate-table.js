function handleEmailResponse(response) {
    $("#email-table").html(response);
}

function filterEmails() {
    console.log('filtered')
    let searchQuery = $("#org-select").val();
    searchQuery = encodeURIComponent(searchQuery);
    let url = "./get-emails?organization=" + searchQuery
    request = $.ajax({
        type: "GET",
        url: url,
        success: handleEmailResponse
    });
}

// connect select change to filterEmails on load
$(document).ready(function() {
    $("select").change(filterEmails);
    console.log("ready")
});