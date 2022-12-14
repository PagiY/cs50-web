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