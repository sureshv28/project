document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const messageContainer = document.createElement('p');
    messageContainer.style.marginTop = '10px';

    const existingMessage = document.querySelector('.login-container p.message');
    if (existingMessage) {
        existingMessage.remove();
    }

    if (!username || !password) {
        messageContainer.textContent = 'Both fields are required.';
        messageContainer.style.color = 'red';
        messageContainer.classList.add('message');
        document.querySelector('.login-container').appendChild(messageContainer);
        return;
    }

    const data = {
        username: username,
        password: password
    };

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/home';
        } else {
            return response.text(); 
        }
    })
    .then(message => {
        if (message) {
            messageContainer.textContent = message;
            messageContainer.style.color = 'red';
            messageContainer.classList.add('message');
            document.querySelector('.login-container').appendChild(messageContainer);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        messageContainer.textContent = 'An error occurred. Please try again later.';
        messageContainer.style.color = 'red';
        messageContainer.classList.add('message');
        document.querySelector('.login-container').appendChild(messageContainer);
    });
});
