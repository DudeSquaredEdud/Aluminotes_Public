document.addEventListener('DOMContentLoaded', function () {
  const generateButton = document.getElementById('gen_button');

  generateButton.addEventListener('click', function () {
    // Disable the button
    generateButton.disabled = true;

    // Add the 'rotate' class to start the animation
    generateButton.classList.add('rotate');

    // Remove the 'rotate' class after the animation ends
    generateButton.addEventListener(
      'animationend',
      function () {
        generateButton.classList.remove('rotate');
      },
      { once: true }
    );

    // Re-enable the button after 5 seconds
    setTimeout(function () {
      generateButton.disabled = false;
    }, 5000);
  });
});
