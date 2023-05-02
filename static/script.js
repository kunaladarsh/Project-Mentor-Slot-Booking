const form = document.querySelector('form');

form.addEventListener('submit', (event) => {
  const usernameInput = document.getElementById('username');
  const passwordInput = document.getElementById('password');

  
if (usernameInput.value === '' || passwordInput.value === '') {
    alert('Please fill in both fields.');
    event.preventDefault();
  }  
});

function signupmessage() {
  alert("SignUp Succesfully Complete...Thank You For SignUp");
}

function msgpers() {
  alert("Personal Details Update Succesfully");
}

function msgproj() {
  alert("project Details Update Succesfully");
}


function msgpass() {
  alert("password Update Succesfully");
}
