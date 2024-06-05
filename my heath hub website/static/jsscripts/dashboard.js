function confirmLogout() {
    if (confirm("Want to log out?")) {
        window.location.href = "{{ url_for('logout') }}";
    }
}

function navigateTo(url) {
    window.location.href = url;
}

