var sdk = apigClientFactory.newClient({});

function record(){
    console.log("here!");
    
    window.SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
    const recognition = new window.SpeechRecognition();

    recognition.onresult = (event) => {
        const speechToText = event.results[0][0].transcript;
        console.log("here");
        console.log(speechToText);
        document.getElementById('search_box').value = speechToText;
        searchPhotos();
        }

    recognition.stop();

    console.log("here2");
    recognition.start();
}

function searchPhotos(){
    search_text = document.getElementById('search_box').value;
    sdk.searchGet({'query':search_text}, {}, {}).then((response) => {
        console.log(response);

        var images = response.data.body;

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
