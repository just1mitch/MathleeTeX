$(document).ready(function() {
    //switch between the login form and signup form
    $(".switch-form").click(function(e) {
        e.preventDefault();
        $("#auth-error").remove(); //removal of any authentication error messages whenever switching forms so users aren't confused when switching back
        $(".auth-container").toggle();
    });

    $("#login-form").submit(function(e) {
        e.preventDefault();
        $("#auth-error").remove(); 

        var boxChecked = $("#remember").is(":checked") ? '1':'0'; //assigned 1 if true, 0 if false
        var formData = {
            username: $("#login-usr").val(),
            password: $("#login-pwd").val(),
            remember: boxChecked
        };
        //formData = JSON.stringify(formData);
        $.ajax({
            type: "POST",
            url: "aaaa", //blank until we have our server routes in place
            data: formData,
            dataType: JSON,
            success: function(response) {
                window.alert("logged in"); //temporary message for now.
                /*
                 * To Do:
                 * 1. Establish login session @ redirect to home page
                 * 2. If "remember me" was checked, give user a cookie to remain logged in.
                  */
            },
            error: function(xhr, status, error) {
                $("#login-pwd").after('<div id="auth-error"></div>');
                if(xhr.status === 401) {
                    $("#auth-error").text('Incorrect Password');
                }
                else {
                    $("#auth-error").text("A problem has occured. Please try again later.");
                }
            }
        });
    });

    $("#signup-form").submit(function(e) {
        e.preventDefault();
        $("#auth-error").remove();

        var pwd1 = $("#signup-pwd").val();
        var pwd2 = $("#pwd-conf").val();
        if(!(pwd1 === pwd2)) {
            $("#pwd-conf").after('<div id="auth-error">Passwords do not match.</div>');
        } else {
            var formData = {
                email: $("#email").val(),
                username: $("#signup-usr").val(),
                password: pwd1,
                pwdConfirm: pwd2
            };
            //formData = JSON.stringify(formData);
            $.ajax({
                type: "POST",
                url: "aaa",
                data: formData,
                dataType: JSON,
                success: function(response) {
                    window.alert("signed up");
                    /*
                     * To Do:
                     * 1. Inform user their account has been successfully created
                     * 2. Establish Login Session upon successful account creation
                     * 3. Redirect to account home page                     
                    */
                },
                error: function(xhr, status, error) {
                    if(xhr.status === 401) { //email already taken
                        $("#email").after('<div id="auth-error">Email is already in use.</div>');
                    } else {
                        $("#pwd-conf").after('<div id="auth-error">A problem has occured during account creation. Please try again later.');
                    }
                }

            });
        }
    });
});