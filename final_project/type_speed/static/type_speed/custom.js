
let time;
let textId;
let currentLetterIndex = 1;
let spelled;
let misspelled;
let words;
let accuracyRate;
let timerInterval;
let scrollDistance;
const allowedChars = /^[A-Za-z0-9.,-]+$/;

$(document).ready(function () {
    $("#myInput").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $("#myTable tr").filter(function () {
            var searchData = $(this).find("td[data-search]").map(function () {
                return $(this).attr("data-search").toLowerCase();
            }).get().join(" ");
            $(this).toggle(searchData.indexOf(value) > -1);
        });
    });
});


document.addEventListener('DOMContentLoaded', function() {

    
    document.querySelector('#speed-test').style.display = 'none';
    document.querySelector('#text-selection').style.display = 'block';
    document.querySelector('#test-result').style.display = 'none';

    const button = document.getElementById("restart-button");
    button.addEventListener('click', () => {
        load_text(textId);
    });


    const textInput = document.getElementById('text_field');
    textInput.addEventListener('keyup', (event) => {
        input_process(event);
    });

    document.getElementById("save-button").addEventListener('click', () => {
        sendData(words, spelled, accuracyRate);
        load_text(textId);
    });

    document.getElementById("again-button").addEventListener('click', () => {
        load_text(textId);
    });

    document.addEventListener('click', () => {
        textInput.focus();
    });

});


function load_text(id) {

    textId = id;
    accuracyRate = 0;
    spelled = 0;
    misspelled = 0;
    words = 0;

    document.querySelector('#speed-test').style.display = 'block';
    document.querySelector('#text-selection').style.display = 'none';
    document.querySelector('#test-result').style.display = 'none';

    const timer = document.getElementById('timer');
    timer.innerHTML = 60;
    time = 2;
    currentLetterIndex = 1;
    clearInterval(timerInterval);
    const message = document.createElement('span');
    message.classList.add('letter');
    message.textContent = 'Text is loading...';

    const textDiv = document.querySelector('#text-div');
    textDiv.innerHTML = '';
    textDiv.append(message);
    scrollDistance = textDiv.scrollTop;

    fetch(`/text/${id}`, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(texts => {
        textDiv.innerHTML = '';
        let letterCounter = 1;
        let value = texts['text'];  
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
    document.querySelector('#text-selection').style.display = 'none';
    document.querySelector('#test-result').style.display = 'block';
    accuracyRate = (spelled / (spelled + misspelled)) * 100;
    if (!isFinite(accuracyRate)) {
        accuracyRate = 0;
    }
    accuracyRate = accuracyRate.toFixed(1);
    accuracyRate = `${accuracyRate}%`;
    document.querySelector('#words-min').innerHTML = words;
    document.querySelector('#chars-min').innerHTML = spelled;
    document.querySelector('#accuracy').innerHTML = accuracyRate;

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
            custom: true,
            textId: textId
        }),
    });
}
