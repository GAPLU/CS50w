document.addEventListener('DOMContentLoaded', function() {


    const tofollow = document.querySelector('#to-follow');
    const tounfollow = document.querySelector('#to-unfollow');
    if (tofollow) {
        document.querySelector('#to-follow').addEventListener('click', () => follow_toggle("follow"))
    } 

    if (tounfollow) {
        document.querySelector('#to-unfollow').addEventListener('click', () => follow_toggle("unfollow"))
    }

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


function follow_toggle(todo) {
    
    const username = document.querySelector('#profile_username').innerHTML

    if (todo === "follow") {
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        fetch(`/users/${username}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                following: "follow"
            })
        })
    }
    else if (todo === "unfollow") {
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        fetch(`/users/${username}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                following: "unfollow"
            })
        })
    }
}