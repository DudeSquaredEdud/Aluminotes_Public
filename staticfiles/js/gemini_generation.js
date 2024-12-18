document.getElementById('gen_button').onclick = function () {
  run();
};

const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

async function run() {
  if (document.getElementById('input_text').value != '') {
    let template = '';

    function add_to_template(option_name, text) {
      if (document.getElementById(option_name).checked) {
        template += text;
      }
    }

    const options = [
      { id: 'summary', text: ' Summarize' },
      { id: 'formal', text: ' Formal' },
      { id: 'academic', text: ' Academic' },
      { id: 'creative', text: ' Creative and Poetic' },
      { id: 'study_notes', text: ' Study notes' },
      { id: 'meeting_notes', text: ' Meeting notes' },
      { id: 'email_and_memo', text: ' Email' },
      { id: 'outline', text: ' Outline' },
      { id: 'story_telling', text: ' Story' },
      { id: 'research_paper', text: ' Research paper' },
      { id: 'report', text: ' Report' },
      { id: 'resume', text: ' Resume' },
    ];

    options.forEach((option) => add_to_template(option.id, option.text));

    prompt = template + ':' + document.getElementById('input_text').value.replace(/"/g, '\\"');
    console.log('Input: ' + prompt);
    const data = {
      prompt: prompt,
      //NOTE: REMOVE THESE LINES IN A FUTURE ISSUE VVVVVVV
      user_type: '{{ user.userprofile.user_type }}',
      user_time: '{{ user.userprofile.last_prompt_time }}',
      user: '{{ user }}',
      //NOTE: REMOVE THESE LINES IN A FUTURE ISSUE ^^^^^^^
    };
    document.getElementById('output_text').innerHTML = '';
    fetch('/reshape/', {
      method: 'POST',
      body: JSON.stringify(data),
      headers: { 'X-CSRFToken': csrftoken },
    }).then((response) => {
      // Handle the response as a stream
      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');
      let accumulatedData = '';

      const processChunk = async () => {
        const { done, value } = await reader.read();
        if (done) {
          console.log('Stream finished');
          return;
        }
        const decodedChunk = decoder.decode(value);
        const dataChunks = decodedChunk.split('\n');

        for (const chunk of dataChunks) {
          if (chunk) {
            try {
              const jsonData = JSON.parse(chunk);
              if (jsonData.toString().substring(0, 3) == 'ERR') {
                AlertBox.show(jsonData.toString().split('ERR: ')[1]);
                return;
              }
              accumulatedData += jsonData;
              console.log(jsonData);

              if (document.getElementById('bionic_reading').checked) {
                // Process accumulatedData to bold the first part of each word
                try {
                  const processedData = accumulatedData.replace(/\b([a-zA-Z]+)/g, (match, p1) => {
                    // Determine how much of the word to bold
                    const boldLength = Math.ceil(p1.length / 2);
                    return '**' + p1.slice(0, boldLength) + '**' + p1.slice(boldLength);
                  });
                  document.getElementById('output_text').innerHTML = marked.parse(processedData);
                } catch (error) {
                  console.error('Error bolding letters:', error);
                  AlertBox.show('Error bolding letters:');
                }
              } else {
                document.getElementById('output_text').innerHTML = marked.parse(accumulatedData);
                document.getElementsByName('output_text')[1].innerHTML =
                  document.getElementById('output_text').innerHTML;
              }
            } catch (error) {
              console.error('Error parsing JSON chunk:', error);
              AlertBox.show('Error parsing JSON chunk:');
            }
          }
        }
        processChunk(); // Call itself recursively to process next chunk
      };
      processChunk();
      accumulatedData = ''; // Reset for next note
    });
  } // The error for not having anything in the input
  else {
    AlertBox.show('Please include some text in the input area');
  }
}
