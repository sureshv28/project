document.getElementById('registrationForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const message = document.getElementById('message');

    message.textContent = '';

    if (password !== confirmPassword) {
        message.textContent = 'Passwords do not match!';
        message.style.color = 'red';
        return;
    }

    const data = {
        username: username,
        email: email,
        password: password
    };

    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            message.textContent = 'Registration successful!';
            message.style.color = 'green';
            setTimeout(() => {
                window.location.href = '/login'; 
            }, 2000);
        } else {
            message.textContent = data.message || 'Registration failed. Please try again.';
            message.style.color = 'red';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        message.textContent = 'An error occurred. Please try again.';
        message.style.color = 'red';
    });
});
