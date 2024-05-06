function switchContainers(a, b) {
    $("#"+ a + "-form").hide();
    $("#" + b + "-form").show();
    sessionStorage.setItem("lastForm", b);
}

$(document).ready(function() {
    //Define the Regular Expressions to validate inputs on client-end (Length is checked in the HTML form)
    const userRegex = /^\w{3,20}$/; //requires one or more: Letters, numbers and underscores
    const pwdRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\\w\\d\\s]).{8,}$/; //requires at least one: lowercase, uppercase, digit and special character (character that isn't alphanumeric or whitespace)

    
    //Hide Form based on whichever option was last selected
    if(sessionStorage.getItem('lastForm') === "signup"){
        $('#switch').prop("checked", true);
        switchContainers("login", "signup");
    } 
    $('#switch').change(function() {
        if(sessionStorage.getItem("lastForm") === "signup") {
            switchContainers("signup", "login");
        } else {
            switchContainers("login", "signup");
        }
    });

    $('#loginformelement').submit(function() {
        var $errorContainer = $(this).find(".error-section");
        //remove any prior error messages
        $errorContainer.empty();
        const validUser = userRegex.test($("#username").val().trim());
        if(!validUser) {
            $errorContainer.append("<p class='error-message-login'>Invalid username</p>");
        }
        const validPwd = pwdRegex.test($("#password").val().trim());
        if(!validPwd) {
            $errorContainer.append("<p class='error-message-login'>Invalid password</p>");
        }
        if(validPwd && validUser) {
            //credentials are valid - continue with submission
            return;
        } 
        //credentials are invalid OR validation failed in some way - prevent submission
        return false;
    });

    $('#signupformelement').submit(function() {
        var $errorContainer = $(this).find(".error-section");
        $errorContainer.empty();
        //validate username
        const validUser = userRegex.test($("#setusername").val().trim());
        if(!validUser) {
            $errorContainer.append("<p class='error-message-signup'>Username must be between 3 and 20 characters in length and may only contain Letters, numbers and underscores.</p>");
        }
        //validate password
        const validPwd = pwdRegex.test($("#createpassword").val().trim());
        if(!validPwd) {
            $errorContainer.append("<p class='error-message-signup'>Password must be at least 8 characters in length, and must contain:<br>\
            - At least one uppercase letter<br>\
            - At least one lowercase letter<br>\
            - At least one digit<br>\
            - At least one special character</p>");
        }
        //validate confirm password
        const validConfirm = ($("#createpassword").val() === $("#confirmpassword").val());
        if(!validConfirm) {
            $errorContainer.append("<p class='error-message-signup'>Passwords do not match</p>");
        }
        if(validUser && validPwd && validConfirm) {
            //credentials are valid - send request
            return;
        }
        //credentials are invalid OR validation failed - prevent submission
        return false;
    });
});