// Get references to form elements
const form = document.querySelector('form');
const loginSubmit = document.getElementById("loginSubmit")
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');

const firstnameInput = document.getElementById('firstname');
const lastnameInput = document.getElementById('lastname');
const setusernameInput = document.getElementById('setusername');
const createpasswordInput = document.getElementById('createpassword');
const confirmpasswordInput = document.getElementById('confirmpassword');
const signUpSubmit = document.getElementById("signUpSubmit")

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
        const firstName = firstnameInput.value;
        const lastName = lastnameInput.value;
        const username = setusernameInput.value;
        const createPassword = createpasswordInput.value;
        const confirmPassword = confirmpasswordInput.value;

        // Do something with the values...
        console.log("NEW USER:")
        console.log('Name:', firstName, " ", lastName);
        console.log('Username:', username);
        console.log("Password:", createPassword)
    });
}