document.addEventListener('DOMContentLoaded', function (){

    const newPostForm = document.querySelector('#new-post-form');
    if (newPostForm) {
        document.querySelector('#new-post-form').addEventListener('submit', post);
    } 


});

function post(event) {
    event.preventDefault();
    const body = document.querySelector('#post-body').value;
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch('/create_post', {
        method: 'POST', 
        body: JSON.stringify({
            body: body
        }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        }
    })
    .then(response => response.json())
    .then(() => {
        document.querySelector('#post-body').value = '';
        location.reload();
    });

}
