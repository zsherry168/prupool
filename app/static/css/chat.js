document.getElementById('send-button').addEventListener('click', function() {
  var messageInput = document.getElementById('message-input');
  var messageText = messageInput.value.trim();

  if (messageText !== '') {
      var messageContainer = document.createElement('div');
      messageContainer.className = 'message sent';
      
      var messageParagraph = document.createElement('p');
      messageParagraph.textContent = messageText;
      
      var messageImage = document.createElement('img');
      messageImage.src = 'https://news.prudential.com/files/images/executive/high_res/LowreyCharles_Bio.jpg';
      messageImage.alt = 'You';

      messageContainer.appendChild(messageParagraph);
      messageContainer.appendChild(messageImage);

      document.querySelector('.chat-messages').appendChild(messageContainer);
      messageInput.value = '';
      document.querySelector('.chat-messages').scrollTop = document.querySelector('.chat-messages').scrollHeight;
  }
});

document.getElementById('message-input').addEventListener('keypress', function(event) {
  if (event.key === 'Enter') {
      document.getElementById('send-button').click();
  }
});
