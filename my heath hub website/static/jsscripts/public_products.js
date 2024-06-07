/*document.addEventListener('DOMContentLoaded', () => {
    const instructionLink = document.querySelector('.order-instruction-link');
    const instructionPopup = document.querySelector('.instruction-popup');

    instructionLink.addEventListener('mouseover', () => {
        instructionPopup.style.top = '0';
    });

    instructionLink.addEventListener('mouseout', () => {
        instructionPopup.style.top = '-100%';
    });

    instructionPopup.addEventListener('click', () => {
        instructionPopup.style.top = '0';
    });

    instructionPopup.addEventListener('mouseout', () => {
        instructionPopup.style.top = '-100%';
    });
});
*/

document.addEventListener('DOMContentLoaded', () => {
    const instructionLink = document.querySelector('.order-instruction-link');
    const instructionPopup = document.querySelector('.instruction-popup');

    instructionLink.addEventListener('mouseenter', () => {
        instructionPopup.style.top = '0';
    });

    instructionLink.addEventListener('mouseleave', () => {
        instructionPopup.style.top = '-50%';
    });

    instructionPopup.addEventListener('mouseenter', () => {
        instructionPopup.style.top = '0';
    });

    instructionPopup.addEventListener('mouseleave', () => {
        instructionPopup.style.top = '-50%';
    });
});
