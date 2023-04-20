const form = document.querySelector('form');

form.addEventListener('submit', (event) => {
  const usernameInput = document.getElementById('username');
  const passwordInput = document.getElementById('password');

  
if (usernameInput.value === '' || passwordInput.value === '') {
    alert('Please fill in both fields.');
    event.preventDefault();
  }  
});
