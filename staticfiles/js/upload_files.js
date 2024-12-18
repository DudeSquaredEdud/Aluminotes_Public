async function processFileInput(file) {
  ftype = file.type;
  fname = file.name;
  if (ftype === 'text/plain') {
    var reader = new FileReader();
    reader.readAsText(file, 'UTF-8');
    reader.onload = (readerEvent) => {
      var content = readerEvent.target.result;
      document.getElementById('input_text').innerHTML = content;
    };
  } else {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const formData = new FormData();
    formData.append('file', file);
    fetch('/readfile/', {
      method: 'POST',
      body: formData,
      headers: { 'X-CSRFToken': csrftoken },
    }).then((response) => {
      if (response.status == 400) {
        response.text().then((text) => {
          document.getElementById('output_text').innerHTML = JSON.parse(text).error;
        });
        return;
      }
      response.text().then((text) => {
        document.getElementById('input_text').innerHTML = text;
        console.log(text);
      });
      return;
    });
  }
}
document.getElementById('upload').onclick = function () {
  // open the file dialog
  var input = document.createElement('input');
  input.type = 'file';
  input.accept = '.txt, .pdf, .docx';
  // update the content when the file is opened
  input.onchange = (e) => {
    var file = e.target.files[0];
    if (file.size > 5 * 1024 * 1024) {
      // 5 MB limit
      document.getElementById('output_text').innerHTML = 'File size exceeds 5 MB limit';
      return;
    }
    processFileInput(file);
  };
  input.click();
};
