document.addEventListener('DOMContentLoaded', function () {
  const audioPlayer = document.getElementById('audio_player');
  const playButton = document.querySelector('.play-button');
  const outputText = document.getElementById('output_text');

  let speechSynthesisInstance = null;

  playButton.addEventListener('click', function () {
    if (audioPlayer.paused || audioPlayer.ended) {
      audioPlayer.play();
      playButton.querySelector('i').classList.remove('fa-play');
      playButton.querySelector('i').classList.add('fa-pause');

      if (!speechSynthesisInstance) {
        convertTextToSpeech();
      } else {
        resumeSpeech();
      }
    } else {
      audioPlayer.pause();
      playButton.querySelector('i').classList.remove('fa-pause');
      playButton.querySelector('i').classList.add('fa-play');

      if (speechSynthesisInstance) {
        pauseSpeech();
      }
    }
  });

  function convertTextToSpeech() {
    const text = document.getElementById('output_text').innerText;
    if (text) {
      speechSynthesisInstance = new SpeechSynthesisUtterance(text);
      speechSynthesisInstance.onend = function () {
        playButton.querySelector('i').classList.remove('fa-pause');
        playButton.querySelector('i').classList.add('fa-play');
        speechSynthesisInstance = null;
      };
      speechSynthesis.speak(speechSynthesisInstance);
    }
  }

  function pauseSpeech() {
    if (speechSynthesisInstance) {
      speechSynthesis.pause();
    }
  }

  function resumeSpeech() {
    if (speechSynthesisInstance) {
      speechSynthesis.resume();
    }
  }

  function stopSpeech() {
    if (speechSynthesisInstance) {
      speechSynthesis.cancel();
      speechSynthesisInstance = null;
    }
  }
});
