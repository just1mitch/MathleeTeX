$(document).ready(function() {
    $('a.nav-link').on('click', function(e) {
    e.preventDefault();
    localStorage.setItem('lastForm', 'login');
    var url = $(this).attr('href');
    $('#main-content').addClass('content-animation');
    setTimeout(function() {
      window.location.href = url;
    }, 500);
  });
});