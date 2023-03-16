
let currentLetterIndex = 1;
const allowedChars = /^[A-Za-z0-9.,-]+$/;

document.addEventListener('DOMContentLoaded', function() {

    load_text();
    const button = document.getElementById("refresh-button");
    button.addEventListener('click', () => load_text())

    const textInput = document.getElementById('text_field');
    textInput.addEventListener('keyup', (event) => input_process(event));

    document.addEventListener('click', () => {
        textInput.focus();
    });


});


function load_text() {

    currentLetterIndex = 1;
    const message = document.createElement('span');
    message.classList.add('letter');
    message.textContent = 'Text is loading...';

    const textDiv = document.querySelector('#text-div');
    textDiv.innerHTML = '';
    textDiv.append(message);

    const options = {
        method: 'GET',
        headers: {
            'X-RapidAPI-Key': '068a260094msh415d94a551705eap17f1f8jsncc894abd8492',
            'X-RapidAPI-Host': 'hargrimm-wikihow-v1.p.rapidapi.com'
        }
    };

    fetch('https://hargrimm-wikihow-v1.p.rapidapi.com/steps?count=100', options)
    .then(response => response.json())
    .then(texts => {
        textDiv.innerHTML = '';
        let letterCounter = 1;
        for (const key in texts) {
            if (texts.hasOwnProperty(key)) {
                const value = texts[key];
                for (let i = 0; i < value.length; i++) {
                    const letter = value[i];
                    if (letter.match(allowedChars) || letter === ' ') {
                        const element = document.createElement('span');
                        element.classList.add('letter');
                        element.id = `letter${letterCounter}`;
                        element.textContent = letter;
                        textDiv.append(element);
                        
                        if (letter == ' ') {
                            const zeroWidthSpaceElement = document.createElement('span');
                            zeroWidthSpaceElement.innerHTML = '&ZeroWidthSpace;';
                           textDiv.append(zeroWidthSpaceElement);
                        }

                        letterCounter++;
                    }
                }
            }
        }
        document.getElementById('letter1').classList.add('orange');
    });

}

function input_process(event) {

    const key = event.key;

    if (key === 'Shift') {
        return;
    }    

    if (key === 'Alt' || key === 'Tab') {
        event.preventDefault();
        return;
    }
       
    if (!allowedChars.test(key) && key !== ' ') {
        event.preventDefault();
        return;
    }

    if (allowedChars.test(key) || key === ' ') {

        const currentLetter = document.getElementById(`letter${currentLetterIndex}`);
        const nextLetter = document.getElementById(`letter${currentLetterIndex + 1}`)

        if (currentLetter) {

            if (currentLetter.innerHTML === key) {
                console.log("equal")
                currentLetter.classList.remove('orange');
                currentLetter.classList.remove('red');
                currentLetter.classList.add('green')
                nextLetter.classList.add('orange');
                currentLetterIndex++;
            }
            else {
                currentLetter.classList.remove('orange');
                currentLetter.classList.add('red')
            }
        }
    }
}