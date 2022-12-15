window.addEventListener('DOMContentLoaded', (event) => { load() });

function load(){
  let postBtns = document.querySelectorAll('.post-buttons')
  
  postBtns.forEach((btn) => {

    let editBtn = btn.querySelector('#edit-post')
    if(editBtn !== null){
      btn.querySelector('#edit-post').addEventListener('click', () => {
        editPost(btn.parentNode.id)
      })
    }

    let likeBtn = btn.querySelector('#like-post')
    if(likeBtn !== null){
      btn.querySelector('#like-post').addEventListener('click', () => {
        likePost(btn.parentNode.id)
      })
    }

  })
}

function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
}

function editPost(post_id){
  let post = document.getElementById(post_id);
  let text = post.querySelector('.card-text').innerHTML
  
  let prevContent = post.innerHTML;

  post.querySelector('.post-content').innerHTML = `
    <textarea id = "editing-post" class="form-control">${text}</textarea>
  `

  post.querySelector('.post-buttons').innerHTML = `
    <button id = "finalize-button" class = "btn btn-primary">Post</button>
    <button id = "cancel-button"   class = "btn btn-primary">Cancel</button>
  `
  
  post.querySelector('#finalize-button').addEventListener('click', () => {

    let new_text = document.querySelector('#editing-post').value

    
    fetch(`/post`, {
      method: "PUT",
      credentials: 'same-origin',
      headers: {
        "X-CSRFToken": getCookie("csrftoken")
      },
      body: JSON.stringify({
        post_id: post_id,
        text: new_text,
        type: "edit"
      })
    })
    .then(response => {
      if(response.status == 200){
        post.innerHTML = prevContent;
        post.querySelector('.card-text').innerHTML = new_text;
        load();
      }
    })
    
  })

  post.querySelector('#cancel-button').addEventListener('click', () => {
    post.innerHTML = prevContent;
    load();
  })

}

function likePost(post_id){
  let post = document.getElementById(post_id);
  let content = post.querySelector('#like-post').innerHTML;
  let counts = parseInt(post.querySelector('#like-counts').innerHTML);

  let element = document.createElement('span')
  element.setAttribute('class', "badge text-bg-secondary")
  element.setAttribute('id', "like-counts")

  fetch(`/post`, {
    method: "PUT",
    credentials: 'same-origin',
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
    body: JSON.stringify({
      post_id: post_id,
      type: "like"
    })
  })
  .then(response => {
    if(response.status == 200){
      post.querySelector('#like-post').innerHTML = ``;
      if(content.includes('Like')){
        counts+=1;
        element.appendChild(document.createTextNode(counts.toString()));
        post.querySelector('#like-post').append(document.createTextNode(`Unlike`))
        post.querySelector('#like-post').append(element)

      }
      else{
        counts-=1;
        element.appendChild(document.createTextNode(counts.toString()));
        post.querySelector('#like-post').append(document.createTextNode(`Like`))
        post.querySelector('#like-post').append(element)
        
      }
    }
  })

}

