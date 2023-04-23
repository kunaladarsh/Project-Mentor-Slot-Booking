const form = document.querySelector('form');

form.addEventListener('submit', (event) => {
  const usernameInput = document.getElementById('username');
  const passwordInput = document.getElementById('password');

  
if (usernameInput.value === '' || passwordInput.value === '') {
    alert('Please fill in both fields.');
    event.preventDefault();
  }  
});



function msgpers() {
  alert("Personal Details Update Succesfull");
}

function msgproj() {
  alert("project Details Update Succesfull");
}


function msgpass() {
  alert("password Update Succesfull");
}
