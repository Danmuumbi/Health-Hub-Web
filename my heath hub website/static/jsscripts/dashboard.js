/*document.addEventListener('DOMContentLoaded', function() {
    // Function to handle navigation
    function navigateTo(url) {
        window.location.href = url;
    }

    // Logout confirmation
    function confirmLogout() {
        if (confirm("Are you sure you want to logout?")) {
            navigateTo("/logout");
        }
    }

    // Fetch and display latest news from an API
    async function fetchLatestNews() {
        try {
            const response = await fetch('https://www.medicalnewstoday.com/'); // Replace with actual news API URL
            const newsData = await response.json();

            const newsSection = document.getElementById('latest-news');
            newsSection.innerHTML = '<ul>' + newsData.map(news => `<li>${news.title}</li>`).join('') + '</ul>';
        } catch (error) {
            console.error('Error fetching news:', error);
            const newsSection = document.getElementById('latest-news');
            newsSection.innerHTML = '<p>Failed to load news. Please try again later.</p>';
        }
    }

    // Call fetchLatestNews to populate the news section
    fetchLatestNews();
});
*/

function confirmLogout() {
    if (confirm('Are you sure you want to logout?')) {
        window.location.href = "{{ url_for('logout') }}";
    }
}

function navigateTo(url) {
    window.location.href = url;
}

