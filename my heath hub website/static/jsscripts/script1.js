document.getElementById('loginButton').addEventListener('click', function() {
    var emailUsername = document.getElementById('emailUsername').value;
    var password = document.getElementById('password').value;

    if (emailUsername === "user@example.com" && password === "password") { // Mock login validation
        alert("Login successful!");
        // Redirect to homepage or dashboard
    } else {
        alert("Enter correct information or sign in");
    }
});

document.getElementById('forgotPassword').addEventListener('click', function() {
    var email = prompt("Please enter your email:");
    if (email) {
        // Simulate sending an email
        alert("A new password has been sent to your email.");
    }
});

document.getElementById('needHelp').addEventListener('click', function() {
    var helpInfo = "To sign in, enter your email/username and password. If you don't have an account, click 'Create an account'. If you need further assistance, contact support at support@healthhub.com.";
    alert(helpInfo);
});
