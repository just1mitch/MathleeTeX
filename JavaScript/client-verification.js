$(document).ready(function() {
    $("div.swapForm:nth-of-type(2)").hide(); //Hides the signup form initially so Login form is shown first.
    $("button.swapForm").click(function() {
        $('div.swapForm').toggle();
    });

    $('#signupForm').submit(function() {
        //process signup form
        window.alert("Signed up!");
    });

    $('#loginForm').submit(function() {
        //process login form
        window.alert("Logged in!");
    });
});