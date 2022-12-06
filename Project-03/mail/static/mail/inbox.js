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
  
  document.getElementById("compose-form").addEventListener("submit", function(event){
    event.preventDefault()
  }, true);

  document.querySelector('#send-email').onclick = (e) => {
    
    e.preventDefault();

    let recipients = document.querySelector('#compose-recipients').value;
    let subject = document.querySelector('#compose-subject').value;
    let body = document.querySelector('#compose-body').value;

    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body
      })
    })
    .then(response => response.json())
    .then(result => {
      document.querySelector('#alerts').innerHTML= result.message;
      load_mailbox('sent');
    });

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

    //append to emails
    emails.forEach(email => {

      //show to inbox if not archived
      if(!email.archived || mailbox === 'inbox'){
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
      }
      //show everything else if not inbox
      else{
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
      }
      
      
    })
  });

  //if an email is clicked, get its id
  element.addEventListener('click', function(e) {
    open_mail(e.target.id, mailbox)
  });

  document.querySelector('#emails-view').append(element);

} 

function open_mail(id, mailbox){
  
  const header = document.createElement('div');
  const buttons = document.createElement('div');
  const body = document.createElement('div');

  const replyButton = document.createElement('button');
  const archiveButton = document.createElement('button');
  const unArchiveButton = document.createElement('button');

  replyButton.setAttribute('id', 'reply');
  replyButton.setAttribute('class', 'btn btn-sm btn-outline-primary');
  replyButton.setAttribute('type', 'button');
  replyButton.appendChild(document.createTextNode("Reply"));

  archiveButton.setAttribute('id', 'archive');
  archiveButton.setAttribute('class', 'btn btn-sm btn-outline-primary');
  archiveButton.setAttribute('type', 'button');
  archiveButton.appendChild(document.createTextNode("Archive"));

  unArchiveButton.setAttribute('id', 'archive');
  unArchiveButton.setAttribute('class', 'btn btn-sm btn-outline-primary');
  unArchiveButton.setAttribute('type', 'button');
  unArchiveButton.appendChild(document.createTextNode("Unarchive"));

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

    header.innerHTML = `
      <b>From: </b> ${email.sender}  <br>
      <b>To: </b> ${email.recipients} <br>
      <b>Subject: </b>${email.subject} <br>
      <b>Timestamp: </b>${email.timestamp} <br>
    `

    buttons.appendChild(replyButton);

    if(mailbox !== 'sent'){
      if(email.archived){
        buttons.appendChild(unArchiveButton)
      }
      else{
        buttons.appendChild(archiveButton)
      }   
    } 
    
    body.innerHTML = `
      <hr>
      <p>${email.body}</p>
    ` 
  
  });
  
  replyButton.onclick = () => {reply_email(id)}

  archiveButton.onclick = () => {archive_email(id)}

  unArchiveButton.onclick = () => {unarchive_email(id)}

  document.querySelector('#emails-view').innerHTML = '';
  document.querySelector('#emails-view').append(header);
  document.querySelector('#emails-view').append(buttons);
  document.querySelector('#emails-view').append(body);
}

function archive_email(id){

  let route = '/emails/' + id

  //set archived to true
  fetch(route, {
    method: 'PUT',
    body: JSON.stringify({
        archived: true
    })
  })
  .then(() => {
    load_mailbox('inbox')
  })
}

function unarchive_email(id){
  let route = '/emails/' + id

  //set archived to false
  fetch(route, {
    method: 'PUT',
    body: JSON.stringify({
        archived: false
    })
  })
  .then(() => {
    load_mailbox('inbox')
  })
}

function reply_email(id){

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  let route = '/emails/' + id
  fetch(route)
  .then(response => response.json())
  .then(email => {
    
    //Update composition fields based on recipients and subject
    document.querySelector('#compose-recipients').value = email.sender;
    document.querySelector('#compose-subject').value = `Re: `+email.subject;
    document.querySelector('#compose-body').value = `On ${email.timestamp}, ${email.sender} wrote: "${email.body}"`;
    
  })

  document.getElementById("compose-form").addEventListener("submit", function(event){
    event.preventDefault()
  }, true);

  document.querySelector('#send-email').onclick = () => {
    
    let recipients = document.querySelector('#compose-recipients').value;
    let subject = document.querySelector('#compose-subject').value;
    let body = document.querySelector('#compose-body').value;

    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body
      })
    })
    .then(response => response.json())
    .then(result => {
        document.querySelector('#alerts').innerHTML= result.message;
        load_mailbox('sent');
    });

  }

}