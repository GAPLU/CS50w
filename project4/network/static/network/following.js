document.addEventListener('DOMContentLoaded', function (){

    const newPostForm = document.querySelector('#new-post-form');
    if (newPostForm) {
        document.querySelector('#new-post-form').addEventListener('submit', post);
    } 

    load_index();

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


function load_index() {

    document.querySelector('#posts-view').style.display = 'block'

    fetch('/posts/following')
    .then(response => response.json())
    .then(posts => {
        posts.forEach(post => {
            const element = document.createElement('div');
            element.classList.add('single-post');
            element.innerHTML = `
            <div class="post-sender"><h5><b>${post.user}</b></h5></div>
            <div class="post-body">${post.body}</div>
            <div class="post-timestamp"><span>${post.timestamp}</span></div>
            <div class="likes">${post.likes}</div>
            `;

            document.querySelector('#all-posts').append(element)
        });

    });


}