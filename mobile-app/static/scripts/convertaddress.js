// Converts address tags to google map links
$(document).ready(function () {
    $('address').each(function () {
        var link = "<a href='http://maps.google.com/maps?q=" + encodeURIComponent( $(this).text() ) + "' target='_blank'>" + $(this).text() + "</a>";
        $(this).html(link);
    });
});