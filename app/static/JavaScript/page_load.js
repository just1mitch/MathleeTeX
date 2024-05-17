$(document).ready(function() {
    $('a').on('click', function(e) {
    e.preventDefault();
    var url = $(this).attr('href');
    $('#main-content').addClass('content-animation');
    setTimeout(function() {
      window.location.href = url;
    }, 500);
  });
});