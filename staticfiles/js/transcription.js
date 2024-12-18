// OUTLINE:
// link the transcribe button to an onclick function
// use that function to:
// - ask permission to use mic
// - begin a recording and save it to a writablestream
// - send audio chunks to the server periodically for real-time transcription
// - update the user's page with the transcribed text as it becomes available

// Global variables
let is_recording = false;
let mic_permission = false;
let mediaRecorder;
let audioChunks = [];
const CHUNK_INTERVAL = 5000; // 5 seconds in milliseconds

// Get the transcribe button element
const transcribe_button = document.getElementById('transcribe');

// Add click event listener to the transcribe button
transcribe_button.onclick = function () {
  if (is_recording) {
    // Stop the recording if one is already running
    stopRecording();
  } else {
    // Start recording
    is_recording = true;
    transcribe_button.style = 'color: red;';

    if (!mic_permission) {
      // Request microphone permission if not already granted
      navigator.mediaDevices
        .getUserMedia({ audio: true })
        .then((stream) => {
          mic_permission = true;
          mediaRecorder = new MediaRecorder(stream);
          startRecording();
        })
        .catch((err) => {
          console.error('Error accessing microphone:', err);
          is_recording = false;
          transcribe_button.style = '';
        });
    } else {
      // If permission is already granted, start recording
      startRecording();
    }
  }
};

// Function to start the recording process
function startRecording() {
  audioChunks = [];

  // Event handler for when audio data is available
  mediaRecorder.ondataavailable = (event) => {
    audioChunks.push(event.data);
  };

  // Event handler for when recording stops
  mediaRecorder.onstop = () => {
    sendAudioChunk();
  };

  // Start the media recorder
  mediaRecorder.start();

  // Set up interval to send chunks periodically
  sendChunksInterval = setInterval(() => {
    if (is_recording) {
      mediaRecorder.stop();
      mediaRecorder.start();
    }
  }, CHUNK_INTERVAL);
}

// Function to stop recording
function stopRecording() {
  clearInterval(sendChunksInterval);
  mediaRecorder.stop();
  is_recording = false;
  transcribe_button.style = '';
}

// Function to send audio chunk to the server
function sendAudioChunk() {
  if (audioChunks.length > 0) {
    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
    sendAudioToServer(audioBlob);
    audioChunks = [];
  }
  console.log('chunk sent');
}

// Function to send recorded audio to the server
function sendAudioToServer(audioBlob) {
  const formData = new FormData();
  formData.append('audio', audioBlob, 'recording.webm');

  // Get the CSRF token from the cookie
  const csrftoken = getCookie('csrftoken');

  // Send a POST request to the server with the audio data
  fetch('/transcribe_audio/', {
    method: 'POST',
    body: formData,
    headers: {
      'X-CSRFToken': csrftoken,
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.transcription) {
        console.log('Transcription:', data.transcription);
        // Update the input text area with the transcription
        const inputText = document.getElementById('input_text');
        inputText.value += (inputText.value ? ' ' : '') + data.transcription;
        document.getElementsByName('input_text')[1].value = inputText.value;
      } else if (data.error) {
        console.error('Transcription error:', data.error);
      }
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

// Function to get CSRF token from cookie
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
