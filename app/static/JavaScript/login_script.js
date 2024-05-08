$(document).ready(function() {
    //Define the Regular Expressions to validate inputs on client-end (Length is checked in the HTML form)
    const userRegex = /^\w{3,20}$/; //requires one or more: Letters, numbers and underscores
    //const pwdRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\\w\\d\\s]).{8,}$/;
    const passwordCriteria = {
        length: { regex: /^.{8,}$/, message: "Password must be at least 8 characters in length." },
        uppercase: { regex: /(?=.*[A-Z])/, message: "Must contain at least one uppercase letter." },
        lowercase: { regex: /(?=.*[a-z])/, message: "Must contain at least one lowercase letter." },
        digit: { regex: /(?=.*\d)/, message: "Must contain at least one digit." },
        specialChar: { regex: /(?=.*[^\\w\\d\\s])/, message: "Must contain at least one special character." }
    }; //requires at least one: lowercase, uppercase, digit and special character (character that isn't alphanumeric or whitespace)

    function switchContainers(a, b) {
        $("#"+ a + "-form").hide();
        $("#" + b + "-form").show();
        sessionStorage.setItem("lastForm", b);
    }
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
        const username = $("#username").val().trim();
        const password = $("#password").val().trim();
        const validUser = userRegex.test(username);
        const validPwd = updatePasswordValidation(password, false);
        // if(!validUser) {
        //     $errorContainer.append("<p class='error-message-login'>Invalid username</p>");
        // }
        // if(!validPwd) {
        //     $errorContainer.append("<p class='error-message-login'>Invalid password</p>");
        // }
        //credentials are valid - continue with submission
        return validPwd && validUser; // if either is false, the form will not submit - bit more streamlined
    });

    $('#signupformelement').submit(function() {
        var $errorContainer = $(this).find(".error-section");
        $errorContainer.empty();
        const username = $("#setusername").val().trim();
        const password = $("#createpassword").val().trim();
        const confirmPassword = $("#confirmpassword").val().trim();
        //validate username
        const validUser = userRegex.test(username);
        //validate password
        const validPwd = updatePasswordValidation(password, true);
        //validate confirm password
        const validConfirm = password === confirmPassword;
        if (!validConfirm) {
            $errorContainer.append("<p class='error-message-signup'><span class='error-cross'>✘</span> Passwords do not match</p>");
        }
        return validUser && validPwd && validConfirm;
    });
    $('#createpassword').on('input', function() {
        updatePasswordValidation($(this).val().trim()); // Validate in real-time as user types
    });

    function updatePasswordValidation(password, display=true) {
        var $errorContainer = $(".error-section");
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