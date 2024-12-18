$(document).ready(function () {
  // Function to enable/disable sliders based on user type
  function toggleSliders(enabled) {
    $(
      '#academic, #creative, #email_and_memo, #story_telling, #research_paper, #report, #resume'
    ).prop('disabled', !enabled);
  }

  // Check user type and toggle sliders initially
  var userType = '{{ user.userprofile.user_type }}';
  if (userType == 0) {
    toggleSliders(false); // Disable sliders for user type 0
  } else {
    toggleSliders(true); // Enable sliders for other user types
  }
});
