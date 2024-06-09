document.addEventListener("DOMContentLoaded", function() {
    const images = document.querySelectorAll(".cover-photo img");
    let currentIndex = 0;

    console.log('Images loaded:', images);

    function showNextImage() {
        console.log('Current index before change:', currentIndex);
        images[currentIndex].classList.remove("active");
        currentIndex = (currentIndex + 1) % images.length;
        images[currentIndex].classList.add("active");
        console.log('Current index after change:', currentIndex);
    }

    setInterval(showNextImage, 5000);

    images.forEach((image, index) => {
        console.log('Adding click event to image:', index);
        image.addEventListener('click', () => {
            console.log('Image clicked:', index);
            /*window.location.href = '../../../templates/news.html';*/
            window.location.href = 'https://www.webmd.com/news/default.htm';



        });
    });

    document.getElementById('lab-results-link').addEventListener('click', function(event) {
        event.preventDefault();
        alert('Please login to see your lab results.');
    });

    document.getElementById('appointments-link').addEventListener('click', function(event) {
        event.preventDefault();
        alert('Please login to book appointments.');
    });

    document.getElementById('immunization-link').addEventListener('click', function(event) {
        event.preventDefault();
        alert('Please login to see your immunization information.');
    });

    document.getElementById('payments-link').addEventListener('click', function(event) {
        event.preventDefault();
        window.location.href = 'https://www.paypal-mobilemoney.com/m-pesa/';
    });

    function goToNewsPage() {
        window.location.href = 'https://www.webmd.com/news/default.htm';
    }

    const newsLink = document.getElementById('news-link');
    newsLink.addEventListener('click', goToNewsPage);
});

document.getElementById('sale-goods').addEventListener('click', function(event) {
    event.preventDefault();
    alert('Please login to advertise and sell with us.');
});
