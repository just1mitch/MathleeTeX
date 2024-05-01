// Get references to form elements
const switchInput = document.getElementById('switch');

const form = document.querySelector('form');
const loginForm = document.getElementById("login-form")
const loginSubmit = document.getElementById("loginSubmit")
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');

const signupForm = document.getElementById("signup-form")
const setusernameInput = document.getElementById('setusername');
const emailInput = document.getElementById('setemail');
const createpasswordInput = document.getElementById('createpassword');
const confirmpasswordInput = document.getElementById('confirmpassword');
const signUpSubmit = document.getElementById("signUpSubmit");

if(switchInput) {
    switchInput.addEventListener('change', function() {
        if (this.checked) {
          loginForm.style.display = 'none';
          signupForm.style.display = 'block';
        } else {
          loginForm.style.display = 'block';
          signupForm.style.display = 'none';
        }
      });
}
if (loginSubmit) {
    // Add event listener to form submission
    loginSubmit.addEventListener('click', function(event) {
        // Prevent the default form submission behavior
        event.preventDefault();

        // Get the values from form inputs and store them as variables
        const username = usernameInput.value;
        const password = passwordInput.value;

        // Do something with the values...
        console.log("LOGIN:")
        console.log('Username:', username);
        console.log('Password:', password);

    
    });
}

if(signUpSubmit) {
    signUpSubmit.addEventListener('click', function(event) {

        // Prevent the default form submission behavior
        event.preventDefault();

        // Get the values from form inputs and store them as variables

        const username = setusernameInput.value;
        const email = emailInput.value;
        const createPassword = createpasswordInput.value;
        const confirmPassword = confirmpasswordInput.value;

        // Do something with the values...
        console.log("NEW USER:")
        console.log('Email:', email);
        console.log('Username:', username);
        console.log("Password:", createPassword)
    });
}