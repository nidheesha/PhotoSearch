
var sdk = apigClientFactory.newClient({});

function searchPhotos(){
    search_text = document.getElementById('search_box').value;
    sdk.searchGet({'query':search_text}, {}, {}).then((response) => {
        console.log(response);

        var images = response.data.body;

        // var html = '';
        // if (images.length == 0) {
        //     html += '<h3>No images found for given tags</h3>';
        // } else {
        //     for (var image in images) {
        //         html += '<img src="' + image + '" witdth="250" height="250" class="thumbnail" /><br><br>';
        //     }
        // }
        // console.log(html);
        // $(html).appendTo($('search_results'));

        if(images.length == 0){
            
            var text = document.createElement('h3');
            text.textContent = 'No images!!'
            console.log('here!')
            document.getElementById('search_result').appendChild(text);
        }
        else{
            for(var image in images){
                var image_element = document.createElement('img');
                image_element.src = images[image];
                image_element.width = '250';
                image_element.height = '250';
                image_element.className = 'thumbnail'
                console.log(image[image]);
                
                document.getElementById('search_result').appendChild(image_element)
            }
        }

    });
    
}

function uploadPhotos(){
    var image = document.getElementById('img').files[0]
    console.log(image);
    console.log(image.type);
    var params = {"filename" : image.name, "bucket" : "bucket2photos", "content-type" : image.type};
    sdk.uploadPut(params, image, {}).then((response)=>{
        console.log(response);
    });
}

var input = document.getElementById('input');
var record = document.getElementById('record');

// setup recognition
const talkMsg = 'Speak now';
// seconds to wait for more input after last
const patience = 5;
var prefix = '';
var isSentence;
var recognizing = false;
var timeout;
var oldPlaceholder = null;
var recognition = new webkitSpeechRecognition();
recognition.continuous = true;
recognition.interimResults = true;

function restartTimer() {
    timeout = setTimeout(function () {
        recognition.stop();
    }, patience * 1000);
}

recognition.onstart = function () {
    oldPlaceholder = input.placeholder;
    input.placeholder = talkMsg;
    recognizing = true;
    restartTimer();
};

recognition.onend = function () {
    recognizing = false;
    clearTimeout(timeout);
    if (oldPlaceholder !== null)
        input.placeholder = oldPlaceholder;
};

recognition.onresult = function (event) {
    clearTimeout(timeout);

    // get SpeechRecognitionResultList object
    var resultList = event.results;

    // go through each SpeechRecognitionResult object in the list
    var finalTranscript = '';
    var interimTranscript = '';
    for (var i = event.resultIndex; i < resultList.length; ++i) {
        var result = resultList[i];
        // get this result's first SpeechRecognitionAlternative object
        var firstAlternative = result[0];
        if (result.isFinal) {
            finalTranscript = firstAlternative.transcript;
        } else {
            interimTranscript += firstAlternative.transcript;
        }
    }
    // capitalize transcript if start of new sentence
    var transcript = finalTranscript || interimTranscript;
    transcript = !prefix || isSentence ? capitalize(transcript) : transcript;

    // append transcript to cached input value
    input.value = prefix + transcript;

    restartTimer();
};


function record(event){
    event.preventDefault();

    // stop and exit if already going
    if (recognizing) {
        recognition.stop();
        return;
    }

    // Cache current input value which the new transcript will be appended to
    var endsWithWhitespace = input.value.slice(-1).match(/\s/);
    prefix = !input.value || endsWithWhitespace ? input.value : input.value + ' ';

    // check if value ends with a sentence
    isSentence = prefix.trim().slice(-1).match(/[\.\?\!]/);

    // restart recognition
    recognition.start();
}

function capitalize(str) {
	return str.charAt(0).toUpperCase() + str.slice(1);
}