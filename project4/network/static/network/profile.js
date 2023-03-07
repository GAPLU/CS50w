document.addEventListener('DOMContentLoaded', function() {

    load_posts();

});

function load_posts() {
    const username = document.querySelector('#profile_username').innerHTML
    fetch(`/posts/${username}`)
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

            document.querySelector('#user-posts').append(element)
        });

    });


}