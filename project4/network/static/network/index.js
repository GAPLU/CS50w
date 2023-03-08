document.addEventListener('DOMContentLoaded', function (){

    const newPostForm = document.querySelector('#new-post-form');
    if (newPostForm) {
        document.querySelector('#new-post-form').addEventListener('submit', post);
    } 

    const editButtons = document.querySelectorAll('.edit');
    editButtons.forEach(button => {
        button.addEventListener('click', () => edit(button));
    });
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


function edit(button) {

    const postId = button.dataset.postid;
    const postBody = button.nextElementSibling;
    const textarea = document.createElement('textarea');
    textarea.classList.add('post-textarea');
    textarea.value = postBody.textContent;
    postBody.replaceWith(textarea);

    const saveBtn = document.createElement('button');
    saveBtn.classList.add('edit', 'btn', 'btn-sm', 'btn-outline-primary');
    saveBtn.setAttribute('id', 'edit-save');
    saveBtn.setAttribute('data-postid', postId);
    saveBtn.textContent = 'Save';
    button.replaceWith(saveBtn)

    saveBtn.addEventListener('click', () => save(button, saveBtn, postId, textarea, postBody))


}


function save(editBtn, saveBtn, postId, textarea, postBody) {

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    postBody.textContent = textarea.value;
    fetch('/update_post', {
        method: 'POST', 
        body: JSON.stringify({
            body: textarea.value,
            id: postId
        }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        }
    })
    .then(response => response.json())
    .then(() => {
        saveBtn.replaceWith(editBtn)
        textarea.replaceWith(postBody)
    });

}


function like(post_id) {
    
    fetch(`/post/${post_id}`, {
        method: "PUT",
        body: "toggle"
    })
    .then(response => response.json())
    .then(data => {
        const likes = document.querySelector(`#likes-${post_id}`);
        likes.innerHTML = `<a onclick="like('${post_id}')">❤️</a>${data.likes}`;
    })
}