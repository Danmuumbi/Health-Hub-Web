/*document.addEventListener("DOMContentLoaded", function() {
    const images = document.querySelectorAll(".cover-photo img");
    let currentIndex = 0;

    function showNextImage() {
        images[currentIndex].classList.remove("active");
        currentIndex = (currentIndex + 1) % images.length;
        images[currentIndex].classList.add("active");
    }

    setInterval(showNextImage, 5000);
});

// Add click event to navigate to news.html
images.forEach(image => {
    image.addEventListener('click', () => {
        window.location.href = 'news.html';
    });
});*/

document.addEventListener("DOMContentLoaded", function() {
    const images = document.querySelectorAll(".cover-photo img");
    let currentIndex = 0;

    // Check if images are selected correctly
    console.log('Images loaded:', images);

    function showNextImage() {
        console.log('Current index before change:', currentIndex);
        images[currentIndex].classList.remove("active");
        currentIndex = (currentIndex + 1) % images.length;
        images[currentIndex].classList.add("active");
        console.log('Current index after change:', currentIndex);
    }

    setInterval(showNextImage, 5000);

    // Add click event to navigate to news.html
    images.forEach((image, index) => {
        console.log('Adding click event to image:', index);
        image.addEventListener('click', () => {
            console.log('Image clicked:', index);
            //window.location.href = "{{ url_for('news') }}";
            window.location.href = "../templates/news.html";
        });
    });
});

