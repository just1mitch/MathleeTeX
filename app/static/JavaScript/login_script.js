$(document).ready(function() {
    //Define the Regular Expressions to validate inputs on client-end (Length is checked in the HTML form)
    const passwordCriteria = {
        length: { regex: /^.{8,}$/, message: "Password must be at least 8 characters in length." },
        uppercase: { regex: /(?=.*[A-Z])/, message: "Must contain at least one uppercase letter." },
        lowercase: { regex: /(?=.*[a-z])/, message: "Must contain at least one lowercase letter." },
        digit: { regex: /(?=.*\d)/, message: "Must contain at least one digit." },
        specialChar: { regex: /(?=.*[\W_])/, message: "Must contain at least one special character." }
    }; //requires at least one: lowercase, uppercase, digit and special character (character that isn't alphanumeric or whitespace)

    function switchContainers(a, b) {
        $("#"+ a + "-form").hide();
        $("#" + b + "-form").show();
        localStorage.setItem("lastForm", b);
    }
    //Hide Form based on whichever option was last selected
    if(localStorage.getItem('lastForm') === "signup"){
        $('#switch').prop("checked", true);
        switchContainers("login", "signup");
    }
    $('#switch').change(function() {
        if(localStorage.getItem("lastForm") === "signup") {
            switchContainers("signup", "login");
        } else {
            switchContainers("login", "signup");
        }
    });

    $('#loginformelement').submit(function(e) {
        e.preventDefault();
        var $errorContainer = $(this).find(".error-section");
        //remove any prior error messages
        $errorContainer.empty();
        const username = $("#username").val().trim();
        const password = $("#password").val().trim();
        const validUser = checkUserLength(username.length, display=false);
        const validPwd = updatePasswordValidation(password, false);
        if(validPwd && validUser) {
            $(this).off('submit').submit(); // disable this handler and submit the form normally
        } else {
            $('#loginformelement')[0].reset();
            $(this).find(".error-section").append("<p class='error'>Please enter valid credentials.</p>");
            $('#login-form').effect("shake");
        }
    });

    $('#signupformelement').submit(function(e) {
        e.preventDefault();
        var $errorContainer = $(this).find(".error-section").eq(1);
        $errorContainer.empty();
        const username = $("#setusername").val().trim();
        const password = $("#createpassword").val().trim();
        const confirmPassword = $("#confirmpassword").val().trim();
        //validate username
        const validUser = checkUserLength(username.length);
        //validate password
        const validPwd = updatePasswordValidation(password, true);
        //validate confirm password
        const validConfirm = password === confirmPassword;
        if (!validConfirm) {
            $errorContainer.append("<p class='error'><span class='error-cross'>✘</span> Passwords do not match</p>");
        }
        if(validUser && validPwd && validConfirm) {
            $(this).off('submit').submit(); //disable the handler and submit the form
        } else {
            $('#signup-form').effect("shake");
        }
    });
    
    $('#setusername').on('input', function() {
        var len = $(this).val().length;
        checkUserLength(len);
    });

    $('#createpassword').on('input', function() {
        updatePasswordValidation($(this).val().trim()); // Validate in real-time as user types
    });


    function checkUserLength(len, display=true) {
        if(display) {
            if(len > 20 || len < 3) {
                $('#userlength').html("<p class='error'><span class='error-cross'>✘</span> Username must be between 3 and 20 characters in length.</p>");
            } else {
                $('#userlength').html("<p class='success'><span class='error-tick'>✔</span> Username is between 3 and 20 characters in length.</p>");
            }
        }
        return (len >= 3 && len <= 20);
    }
    function updatePasswordValidation(password, display=true) {
        var $errorContainer = $("#signupformelement div.error-section").eq(1); //select the second div, so the username length error isn't overwritten
        $errorContainer.empty();
        let isValid = true;
        Object.keys(passwordCriteria).forEach(key => {
            // For each criterion, check if the password meets the criterion
            const criterion = passwordCriteria[key];
            if (!criterion.regex.test(password)) {
                if(display) {
                    // Append error message to the error container
                    $errorContainer.append(`<p class='error'><span class="error-cross">✘</span> ${criterion.message}</p>`);
                }
                isValid = false;
            } else {
                if(display){
                    $errorContainer.append(`<p class='success'><span class="error-tick">✔</span> ${criterion.message}</p>`);            }
       }});
        return isValid;
    }
});