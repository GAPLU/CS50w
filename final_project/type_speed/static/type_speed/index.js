
let time;
let currentLetterIndex = 1;
let spelled;
let misspelled;
let words;
let timerInterval;
let scrollDistance;
const allowedChars = /^[A-Za-z0-9.,-]+$/;
const options = {
    method: 'GET',
    headers: {
        'X-RapidAPI-Key': '068a260094msh415d94a551705eap17f1f8jsncc894abd8492',
        'X-RapidAPI-Host': 'hargrimm-wikihow-v1.p.rapidapi.com'
    }
};

document.addEventListener('DOMContentLoaded', function() {

    load_text();

    const button = document.getElementById("refresh-button");
    button.addEventListener('click', () => {
        load_text();
    });

    const customButton = document.getElementById("custom-button");
    customButton.addEventListener('click', () => {
        custom_text();
    });

    const textInput = document.getElementById('text_field');
    textInput.addEventListener('keyup', (event) => {
        input_process(event);
    });

    document.addEventListener('click', () => {
        textInput.focus();
    });

});


function load_text() {

    spelled = 0;
    misspelled = 0;
    words = 0;

    document.querySelector('#speed-test').style.display = 'block';
    document.querySelector('#test-result').style.display = 'none';

    const timer = document.getElementById('timer');
    timer.innerHTML = 60;
    time = 60;
    currentLetterIndex = 1;
    clearInterval(timerInterval);
    const message = document.createElement('span');
    message.classList.add('letter');
    message.textContent = 'Text is loading...';

    const textDiv = document.querySelector('#text-div');
    textDiv.innerHTML = '';
    textDiv.append(message);
    scrollDistance = textDiv.scrollTop;

    fetch('https://hargrimm-wikihow-v1.p.rapidapi.com/steps?count=100', options)
    .then(response => response.json())
    .then(texts => {
        textDiv.innerHTML = '';
        let letterCounter = 1;
        for (const key in texts) {
            if (texts.hasOwnProperty(key)) {
                let value = texts[key];
                value = value.replace(/[.,-]/g, ' ');
                value = value.replace(/ {2}/g, ' ');

                for (let i = 0; i < value.length; i++) {
                    const letter = value[i].toLowerCase();
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

    if (key === 'Alt' || key === 'Tab' || key === 'Shift' || key === 'CapsLock') {
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

                if (currentLetterIndex === 1) {
                    clearInterval(timerInterval);
                    timerInterval = setInterval(start_timer, 1000);
                    start_timer();
                }

                if (key === ' ') {
                    words +=1;
                }

                currentLetter.classList.remove('orange');
                currentLetter.classList.remove('red');
                currentLetter.classList.add('green')
                nextLetter.classList.add('orange');
                currentLetterIndex++;
                spelled += 1;
                const textDiv = document.getElementById('text-div');
                const threshold = textDiv.offsetHeight * 0.5;
                if (nextLetter.offsetTop - textDiv.scrollTop > threshold) {
                    const scrollDistance = nextLetter.offsetTop - textDiv.offsetTop - threshold;
                    textDiv.scrollTop = scrollDistance;
                }
            }
            else {

                if (currentLetterIndex === 1  && !currentLetter.classList.contains('red')) {
                    clearInterval(timerInterval);
                    timerInterval = setInterval(start_timer, 1000);
                    start_timer();
                }
                currentLetter.classList.remove('orange');
                currentLetter.classList.add('red')
                misspelled += 1;
            }
        }
    }
}


function start_timer() {
    
    const timer = document.getElementById('timer');
    timer.innerHTML = time;
    time--;
   
    if (time < 0){
        clearInterval(timerInterval)
        process_results();
    }
}


function process_results() {

    document.querySelector('#speed-test').style.display = 'none';
    document.querySelector('#custom-text').style.display = 'none';
    document.querySelector('#test-result').style.display = 'block';
    let accuracyRate = (spelled / (spelled + misspelled)) * 100;
    if (!isFinite(accuracyRate)) {
        accuracyRate = 0;
    }
    accuracyRate = accuracyRate.toFixed(1);
    accuracyRate = `${accuracyRate}%`;
    document.querySelector('#words-min').innerHTML = words;
    document.querySelector('#chars-min').innerHTML = spelled;
    document.querySelector('#accuracy').innerHTML = accuracyRate;
    sendData(words, spelled, accuracyRate)

}


function sendData(words, spelled, accuracyRate) {

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    fetch('/results/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
            words: words,
            spelled: spelled,
            accuracyRate: accuracyRate,
        }),
    });
}


function custom_text() {

    document.querySelector('#speed-test').style.display = 'block';
    document.querySelector('#test-result').style.display = 'none';

}