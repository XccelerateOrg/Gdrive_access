// form_script.js
$(document).ready(function() {
  // Hide the loading screen initially
  $('#loading-screen').hide();

  // Handle form submission event
  $('#attendance-form').submit(function(event) {
    event.preventDefault(); // Prevent the form from submitting normally

    // Show the loading screen
    $('#loading-screen').show();

    // Send an AJAX request to submit the form data
    $.ajax({
      type: 'POST',
      url: '/attendance', // Replace with the appropriate endpoint in your Flask app
      data: $(this).serialize(),
      success: function(response) {
        // Hide the loading screen
        $('#loading-screen').hide();

        // Replace the form with the results
//        $('#my-form').hide();
        $('#results-container').html(response);
      },
      error: function(error) {
        console.log('An error occurred:', error);
      }
    });
  });
});