document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  
  
  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

   // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
 
  document.querySelector('#send-email').onClick = () => {
    
    let recipients = document.querySelector('#compose-recipients').value;
    let subject = document.querySelector('#compose-subject').value;
    let body = document.querySelector('#compose-body').value;

    console.log(recipients)
    // fetch('/emails', {
    //   method: 'POST',
    //   body: JSON.stringify({
    //       recipients: recipients,
    //       subject: subject,
    //       body: body
    //   })
    // })
    // .then(response => response.json())
    // .then(result => {
    //     // Print result
    //     console.log(result);
    // });

  }



}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  const element = document.createElement('div');
  element.classList.add('list-group')

  let route = '/emails/' + mailbox
  fetch(route)
  .then(response => response.json())
  .then(emails => {
    console.log(emails)
    //append to emails
    emails.forEach(email => {
      
      if(email.read){
        element.innerHTML += 
        ` <a id = ${email.id} class = "list-group-item list-group-item-action d-flex justify-content-between align-items-center">
          ${email.sender}
          <p>${email.subject}</p>
          <p class = "text-muted">${email.timestamp}</p>
        </a>`
      }
      else{
        element.innerHTML += 
        `<a id = ${email.id} class = "list-group-item list-group-item-action d-flex justify-content-between align-items-center">
          <b>${email.sender}</b>
          <p>${email.subject}</p>
          <p class = "text-muted">${email.timestamp}</p>
        </a>`
      }
      
    })
  });

  //if an email is clicked, get its id
  element.addEventListener('click', function(e) {
    open_mail(e.target.id)
  });


  document.querySelector('#emails-view').append(element);

}

function open_mail(id){
  

  let route = '/emails/' + id

  //set read to true
  fetch(route, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })

  fetch(route)
  .then(response => response.json())
  .then(email => {

    document.querySelector('#emails-view').innerHTML = `
      <b>From: </b> ${email.sender}  <br>
      <b>To: </b> ${email.recipients} <br>
      <b>Subject: </b>${email.subject} <br>
      <b>Timestamp: </b>${email.timestamp} <br>
      <button class="btn btn-sm btn-outline-primary" id="reply">Reply</button>
      <hr>
      <p>${email.body}</p>
    `;

    // ... do something else with email ...
  });
}