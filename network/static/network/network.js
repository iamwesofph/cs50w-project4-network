
function editPost(postId) {
    const postContent = document.querySelector(`#post-${postId}`);
    const postText = postContent.innerHTML;
    postContent.innerHTML = `<textarea rows="4" id="post-${postId}-textarea" class="form-control" name="tweet-content">${postText}</textarea>`;

    const editButton = document.querySelector(`#btn-edit-post-${postId}`);
    editButton.innerHTML = 'Save';
    editButton.setAttribute('onclick', `savePost(${postId})`);
    document.querySelector(`#post-${postId}-textarea`).focus();
}


function savePost(postId) {
    
    // Get new content input by user
    new_content = document.querySelector(`#post-${postId}-textarea`).value;

    fetch(`/update/${postId}`, {
    method: 'PUT',
    body: JSON.stringify({ content: new_content })
  })
  .then(response => response.json())
  .then(data => {
    document.getElementById(`post-${postId}`).innerHTML = data.content;

    const editButton = document.querySelector(`#btn-edit-post-${postId}`);
    editButton.innerHTML = 'Edit';
    editButton.setAttribute('onclick', `editPost(${postId})`);   
  })
  .catch(error => console.error(error));
}


function like(postId) {
    
    // Animate and toggle appearance of the like button
    const heartIcon = document.querySelector(`#heart-icon-${postId}`);
    heartIcon.classList.toggle('liked');

    // Fetch then change the value of the like amount
    const likesAmountLabel = document.querySelector(`#likes-amount-${postId}`); // Get element
    var likesAmount = parseInt(likesAmountLabel.innerHTML, 10);  // Get value
    likesAmount += heartIcon.classList.contains("liked") ? 1 : -1; // Check if the heartIcon has the "liked" class and increment likesAmount if true, otherwise decrement it
    likesAmountLabel.innerHTML = likesAmount; // Set element value

    fetch(`/like/${postId}`, {
        method: 'POST',
        body: JSON.stringify({ post_id: postId,
            })
        })
    .then(response => response.json())
    .then(data => { 
        console.log(data) 

    });
}


// document.addEventListener('DOMContentLoaded', function() {
//     const heartIcon = document.querySelector(".like-button .heart-icon");
//     const likesAmountLabel = document.querySelector(".like-button .likes-amount");

//     let likesAmount = 7;

    // heartIcon.addEventListener("click", () => {
    // if (heartIcon.classList.contains("liked")) {
    //     likesAmount++;
    // } else {
    //     likesAmount--;
    // }

    // likesAmountLabel.innerHTML = likesAmount;
//     });
// });

    // function savePost(postId) {
    //     const editPostTextarea = document.getElementById(`post-${postId}-textarea`);
    //     const postContent = editPostTextarea.value;
    //     fetch(`/update/${postId}`, {
    //       method: 'PUT',
    //       headers: {
    //         'Content-Type': 'application/json',
    //         'X-CSRFToken': '{{ csrf_token }}',
    //       },
    //       body: JSON.stringify({
    //         content: postContent,
    //       })
    //     })
    //       .then(response => response.json())
    //       .then(data => {
    //         document.getElementById(`post-${postId}`).innerHTML = data.content;
            
    //         const editButton = document.querySelector(`#edit-btn-${postId}`);
    //         editButton.innerText = 'Edit';
    //         editButton.onclick = () => {
    //           editPost(postId);
    //         };
    //       })
    //       .catch(error => console.error(error));
    //   }