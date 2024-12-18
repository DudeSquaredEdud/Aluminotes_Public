$('#myForm').submit(function (event) {
  event.preventDefault(); // Prevent default form submission
  var formData = $(this).serialize();
  $('#form-data').val(formData); // Store form data in hidden input
  $.ajax({
    url: '/toolpage_update/',
    type: 'POST',
    data: formData,
  });
  return false;
});

// uncheck the radio boxes
$('.form-check-input').click(function (event) {
  var radio = $(this);
  // if not checked, check it
  if (!radio.is("[checked='checked']")) {
    // uncheck all
    $("[name='saved_user_template']").removeAttr('checked');
    // check the one clicked
    radio.attr('checked', 'checked');
    radio.prop('checked', true);
  }
  // if checked, uncheck it
  else {
    radio.removeAttr('checked');
    radio.prop('checked', false);
    // Set all clear
    update_saved_user_templates([
      false,
      false,
      false,
      false,
      false,
      false,
      false,
      false,
      false,
      false,
      false,
      false,
      false,
    ]);
  }
});

function update_saved_user_templates(templateData) {
  loadableUserTemplate = templateData;
  $('#summary').prop('checked', loadableUserTemplate[0]);
  $('#formal').prop('checked', loadableUserTemplate[1]);
  $('#academic').prop('checked', loadableUserTemplate[2]);
  $('#creative').prop('checked', loadableUserTemplate[3]);
  $('#study_notes').prop('checked', loadableUserTemplate[4]);
  $('#meeting_notes').prop('checked', loadableUserTemplate[5]);
  $('#email_and_memo').prop('checked', loadableUserTemplate[6]);
  $('#outline').prop('checked', loadableUserTemplate[7]);
  $('#story_telling').prop('checked', loadableUserTemplate[8]);
  $('#research_paper').prop('checked', loadableUserTemplate[9]);
  $('#report').prop('checked', loadableUserTemplate[10]);
  $('#resume').prop('checked', loadableUserTemplate[11]);
  $('#bionic_reading').prop('checked', loadableUserTemplate[12]);
}

$('#savedForm').change(function (event) {
  // this submits on form change
  event.preventDefault(); // Prevent default form submission
  var formData = $(this).serialize();
  function string_to_bool(strs) {
    output = [];
    for (str in strs) {
      if (strs[str] == 'True') output.push(true);
      else output.push(false);
    }
    return output;
  }
  update_saved_user_templates(string_to_bool(formData.split('=')[2].split('&')[0].split('%20')));
  return false;
});
