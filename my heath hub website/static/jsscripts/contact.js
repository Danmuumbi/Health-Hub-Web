document.getElementById('contactForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    const data = Object.fromEntries(formData.entries());
    const emailBody = `
        First Name: ${data.first_name}
        Last Name: ${data.last_name}
        Email: ${data.email}
        Phone: ${data.phone}
        Message: ${data.message}
    `;
    window.location.href = `mailto:muumbidaniel0@gmail.com?subject=Contact Us Form Submission&body=${encodeURIComponent(emailBody)}`;
});

