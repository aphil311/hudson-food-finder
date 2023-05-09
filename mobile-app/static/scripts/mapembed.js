// Loads embedded map of organization address
// Author: Yousef Amin
$(document).ready(function(){
    $("address").each(function(){                         
      var embed ="<iframe class='w-100' height='350' frameborder='0' scrolling='no' marginheight='0' marginwidth='0' src='https://maps.google.com/maps?&amp;q=" + encodeURIComponent( $(this).text() ) + "&amp;output=embed'></iframe>";
      $(this).html(embed);
     });
  });