document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', send_post)
  

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
} 

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      emails.forEach(email => {
        const element = document.createElement('div');
        element.classList.add('single-mail');
        element.innerHTML = `
        <div class="email" data-id="${email.id}">
          <div class="email-sender"><b>${email.sender}</b></div>
          <div class="email-subject">${email.subject}</div>
          <div class="email-timestamp">${email.timestamp}</div>
        </div>
        `;

        fetch(`/emails/${email.id}`)
        .then(response => response.json())
        .then(email_by_id => {
            if (email_by_id.read === true) {
              element.style.backgroundColor = 'LightGray';
            }
            else {
              element.style.backgroundColor = 'white';
            }
        });

        element.addEventListener('click', () => email_view(email.id, mailbox))

        document.querySelector('#emails-view').append(element);
      });
  });

}


function send_post(event) {
  event.preventDefault();
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;
  
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(() => {
      load_mailbox('sent');
  });

}


function email_view(email_id, mailbox) {
  document.querySelector('#email-view').innerHTML = '';
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    const element = document.createElement('div');
    element.classList.add('email-view');
    element.innerHTML = `
    <div class="email" data-id="${email.id}">
      <div class="email-sender"><b>From: </b>${email.sender}</div>
      <div class="email-recipient"><b>To: </b>${email.recipients}</div>
      <div class="email-subject"><b>Subject: </b>${email.subject}</div>
      <div class="email-timestamp"><b>Timestamp: </b>${email.timestamp}</div>
      <div class="email-buttons">
        <button onclick="archive(${email.id}, 'archive')" class="btn btn-sm btn-outline-primary" id="archive" style="display: none">Archive</button>
        <button onclick="archive(${email.id}, 'unarchive')" class="btn btn-sm btn-outline-primary" id="unarchive" style="display: none">Unarchive</button>
        <button onclick="reply(${email.id})" class="btn btn-sm btn-outline-primary" id="reply" style="display: none">Reply</button>
      </div>
      <hr>
      <div class="email-body">${email.body}</div>
    </div>
    `;

    document.querySelector('#email-view').append(element);

    if (mailbox != 'inbox') {
      document.querySelector('#reply').style.display = 'none';
      document.querySelector('#archive').style.display = 'none';
    }
    else {
      document.querySelector('#reply').style.display = 'block';
      document.querySelector('#archive').style.display = 'block';
    }

    if (mailbox != 'archive') {
      document.querySelector('#unarchive').style.display = 'none';
    }
    else {
      document.querySelector('#unarchive').style.display = 'block';
    }

    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';


    if (email.read === false) {
      fetch(`emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
      })
    }

  }); 
}


function archive(email_id, action) {
  if (action === 'archive') {
    fetch(`emails/${email_id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: true
      })
    })
    
    .then(() => {
      load_mailbox('inbox')
    });
  }
  else if (action === 'unarchive') {
    fetch(`emails/${email_id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: false
      })
    })

    .then(() => {
      load_mailbox('inbox')
    });
  }

}


function reply(email_id) {
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
  
    // Clear out composition fields
    document.querySelector('#compose-recipients').value = email.sender;
    if (email.subject && email.subject.startsWith('Re: ')) {
      document.querySelector('#compose-subject').value = `${email.subject}`;
    }
    else {
      document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
    }
    document.querySelector('#compose-body').value = `"On ${email.timestamp} ${email.sender} wrote:\n   ${email.body}" \n`;
  });
}