document.addEventListener('DOMContentLoaded', function () {
  const modal = document.getElementById('filenameModal');
  const closeModal = document.getElementsByClassName('close')[0];
  const saveButton = document.getElementById('saveFilename');
  const filenameInput = document.getElementById('filenameInput');

  document.getElementById('download').onclick = function (event) {
    event.preventDefault();

    // Generate default filename
    const date = new Date();
    const dateString =
      String(date.getHours()).padStart(2, '0') +
      '-' +
      String(date.getMinutes()).padStart(2, '0') +
      '-' +
      String(date.getSeconds()).padStart(2, '0') +
      '_' +
      String(date.getDate()).padStart(2, '0') +
      '-' +
      String(date.getMonth() + 1).padStart(2, '0') +
      '-' +
      String(date.getFullYear());
    filenameInput.value = 'reshaped-notes-' + dateString + '.txt';

    // Show the modal
    modal.style.display = 'block';
  };

  closeModal.onclick = function () {
    modal.style.display = 'none';
  };

  saveButton.onclick = function () {
    const fileName = filenameInput.value.replace(/\.txt$/i, '') + '.txt';

    const outputText = document.getElementById('output_text').innerText;
    const blob = new Blob([outputText], { type: 'text/plain;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = fileName;

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);

    // Close the modal
    modal.style.display = 'none';
  };

  window.onclick = function (event) {
    if (event.target == modal) {
      modal.style.display = 'none';
    }
  };
});
