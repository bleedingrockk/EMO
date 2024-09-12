// Get references to the button, floating window, and main content elements
const openButton = document.getElementById('openWindowButton');
const floatingWindow = document.getElementById('floatingWindow');
const closeButton = document.getElementById('closeWindowButton');
const mainContent = document.getElementById('mainContent');

// When the button is clicked, show the floating window and blur the background
openButton.addEventListener('click', () => {
    floatingWindow.style.display = 'block'; // Show the floating window
    mainContent.classList.add('blur'); // Add the blur effect to the background
});

// When the close button is clicked, hide the floating window and remove the blur
closeButton.addEventListener('click', () => {
    floatingWindow.style.display = 'none'; // Hide the floating window
    mainContent.classList.remove('blur'); // Remove the blur effect
});

// Optional: Close the window when the user clicks outside of it
window.addEventListener('click', (event) => {
    if (event.target === floatingWindow) {
        floatingWindow.style.display = 'none'; // Hide the floating window
        mainContent.classList.remove('blur'); // Remove the blur effect
    }
});
