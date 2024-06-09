function togglePassword() {
    const passwordField = document.getElementById('password');
    const togglePasswordText = document.querySelector('.toggle-password');
    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        togglePasswordText.textContent = 'Hide';
    } else {
        passwordField.type = 'password';
        togglePasswordText.textContent = 'Show';
    }
}
