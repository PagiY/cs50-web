document.addEventListener('DOMContentLoaded', function() {


})


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

function editPost(post_id, post_text){
  let id = post_id.toString();
  let post = document.getElementById(id);

  post.innerHTML = `
      <textarea id = "edit-post">${post_text}</textarea>
      <input type="submit" value = "Post" class="btn btn-primary" id="post" onclick = 'edit(${post_id})'/>
      <button class="btn btn-primary" onclick = 'location.reload()' >Cancel</button>
    
  `
}

function edit(post_id){
  let value = document.querySelector('#edit-post').value
  
  fetch(`/edit/${post_id}`, {
    method: "PUT",
    credentials: 'same-origin',
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
    body: JSON.stringify({
      text: value
    })
  })
  .then((data) => {
    location.reload();
  })
}

function likePost(post_id){

    fetch(`/like/${post_id}`, {
        method: "POST",
        credentials: 'same-origin',
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        }
    })
    .then((data) => {
      location.reload();
    });

}

function unlikePost(post_id){

  fetch(`/unlike/${post_id}`, {
    method: "POST",
    credentials: 'same-origin',
    headers: {
        "X-CSRFToken": getCookie("csrftoken")
    }
  })
  .then((data) => {
    location.reload();
  });

}

function follow(user_id){

  fetch(`/follow/${user_id}`, {
    method: "POST",
    credentials: "same-origin",
    headers:{
      "X-CSRFToken": getCookie("csrftoken")
    }
  })
  .then((data) => {
    location.reload();
  })
}

function unfollow(user_id){

  fetch(`/unfollow/${user_id}`, {
    method: "POST",
    credentials: "same-origin",
    headers:{
      "X-CSRFToken": getCookie("csrftoken")
    }
  })
  .then((data) => {
    location.reload();
  })
}